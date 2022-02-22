from decimal import Decimal

import pytest

from ...plugins.manager import get_plugins_manager
from ..fetch import fetch_checkout_info, fetch_checkout_lines


@pytest.fixture
def priced_checkout_factory():
    def factory(checkout):
        manager = get_plugins_manager()
        lines, _ = fetch_checkout_lines(checkout)
        checkout_info = fetch_checkout_info(checkout, lines, [], manager)

        tax = Decimal("1.23")

        for line_info in lines:
            line = line_info.line

            line.total_price = manager.calculate_checkout_line_total(
                checkout_info, lines, line_info, None, []
            ).price_with_sale
            line.unit_price = manager.calculate_checkout_line_unit_price(
                checkout_info,
                lines,
                line_info,
                None,
                [],
            ).price_with_sale

            line.total_price_gross_amount *= tax
            line.unit_price_gross_amount *= tax

            line.save()

        checkout.shipping_price = manager.calculate_checkout_shipping(
            checkout_info, lines, None, []
        )
        checkout.subtotal = manager.calculate_checkout_subtotal(
            checkout_info, lines, None, []
        )
        checkout.total = manager.calculate_checkout_total(
            checkout_info, lines, None, []
        )

        checkout.shipping_price_gross_amount *= tax
        checkout.subtotal_gross_amount *= tax
        checkout.total_gross_amount *= tax
        checkout.save()

        return checkout

    return factory


@pytest.fixture
def priced_checkout_with_item(priced_checkout_factory, checkout_with_item):
    return priced_checkout_factory(checkout_with_item)


@pytest.fixture
def priced_checkout_with_items(priced_checkout_factory, checkout_with_items):
    return priced_checkout_factory(checkout_with_items)


@pytest.fixture
def priced_checkout_with_voucher_percentage(
    priced_checkout_factory, checkout_with_voucher_percentage
):
    return priced_checkout_factory(checkout_with_voucher_percentage)
