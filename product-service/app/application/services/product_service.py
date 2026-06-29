import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.enums.idempotency import (
    IdempotencyOperation,
    IdempotencyStatus,
)
from app.application.exceptions.idempotency import (
    IdempotencyConflictError,
    IdempotencyInProgressError,
)
from app.application.services.idempotency_service import IdempotencyService
from app.infrastructure.cache.idempotency_repository import IdempotencyRepository
from app.infrastructure.cache.product_cache_repository import ProductCacheRepository
from app.infrastructure.models.product_model import ProductModel
from app.infrastructure.repositories.product_repository import ProductRepository
from app.schemas.product import ProductResponse

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(
        self,
        db: AsyncSession,
        product_cache_repository: ProductCacheRepository,
        idempotency_repository: IdempotencyRepository,
    ):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.product_cache_repository = product_cache_repository
        self.idempotency_repository = idempotency_repository

    async def get_products(self) -> list[ProductResponse]:
        cached_products = await self.product_cache_repository.get_products()

        if cached_products is not None:
            return cached_products

        products = await self.product_repository.get_all()

        response_products = [self._to_response(product) for product in products]

        await self.product_cache_repository.set_products(response_products)

        return response_products

    async def create_product(
        self,
        name: str,
        price: int,
        stock_quantity: int,
        idempotency_key: str,
    ) -> ProductResponse:
        request_hash = IdempotencyService.build_request_hash(
            {
                "name": name,
                "price": price,
                "stock_quantity": stock_quantity,
            }
        )

        existing_record = await self.idempotency_repository.get_record(
            operation=IdempotencyOperation.PRODUCT_CREATE,
            idempotency_key=idempotency_key,
        )

        if existing_record is not None:
            if existing_record.request_hash != request_hash:
                logger.info("Product create rejected reason=idempotency_conflict")

                raise IdempotencyConflictError

            if existing_record.status == IdempotencyStatus.COMPLETED:
                logger.info("Product create returned from idempotency cache")

                return ProductResponse(**existing_record.response_data)

            logger.info("Product create rejected reason=idempotency_in_progress")

            raise IdempotencyInProgressError

        was_reserved = await self.idempotency_repository.reserve_operation(
            operation=IdempotencyOperation.PRODUCT_CREATE,
            idempotency_key=idempotency_key,
            request_hash=request_hash,
        )

        if not was_reserved:
            logger.info("Product create rejected reason=idempotency_race")

            raise IdempotencyInProgressError

        try:
            product = await self.product_repository.create_product(
                name=name,
                price=price,
                stock_quantity=stock_quantity,
            )

            await self.db.commit()
            await self.db.refresh(product)

            response_product = self._to_response(product)

            await self.product_cache_repository.delete_products()

            await self.idempotency_repository.save_completed_response(
                operation=IdempotencyOperation.PRODUCT_CREATE,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
                response_data=self._response_to_dict(response_product),
            )

            logger.info(
                "Product created product_id=%s name=%s",
                product.id,
                product.name,
            )

            return response_product

        except Exception:
            await self.db.rollback()

            await self.idempotency_repository.delete_record(
                operation=IdempotencyOperation.PRODUCT_CREATE,
                idempotency_key=idempotency_key,
            )

            logger.exception("Product create failed reason=unexpected_error")

            raise

    def _to_response(self, product: ProductModel) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock_quantity=product.stock_quantity,
        )

    def _response_to_dict(self, product: ProductResponse) -> dict:
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
        }
