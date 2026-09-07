from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal

class Faq(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    category_id: int | None = Field(default=None, alias="categoryId")
    question: str
    answer: str
    status: int = 1
    use_count: int = Field(default=0, alias="useCount")


class FaqPage(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    records: list[Faq] = Field(default_factory=list)
    total: int = 0
    size: int = 0
    current: int = 1
    pages: int = 0


class JavaResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: int
    message: str | None = None
    data: FaqPage | None = None


class JavaFaqResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: int
    message: str | None = None
    data: Faq | None = None
class CartGoods(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    good_id: int | None = Field(default=None, alias="goodId")
    goods_name: str | None = Field(default=None, alias="goodsName")
    price: Decimal | None = None
    num: int | None = None


class ShoppingOrder(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    payment: Decimal | None = None
    status: int | None = None
    create_time: datetime | None = Field(default=None, alias="createTime")
    payment_time: datetime | None = Field(default=None, alias="paymentTime")
    consign_time: datetime | None = Field(default=None, alias="consignTime")
    shipping_name: str | None = Field(default=None, alias="shippingName")
    shipping_code: str | None = Field(default=None, alias="shippingCode")
    cart_goods: list[CartGoods] = Field(default_factory=list, alias="cartGoods")


class JavaOrdersResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: int
    message: str | None = None
    data: list[ShoppingOrder] = Field(default_factory=list)
class JavaOrderResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: int
    message: str | None = None
    data: ShoppingOrder | None = None


class JavaCurrentUserResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: int
    message: str | None = None
    data: int | None = None
