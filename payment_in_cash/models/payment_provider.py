from odoo import fields, models, api
from odoo.addons.payment_in_cash.const import SUPPORTED_CURRENCIES


class PaymentProviderCash(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payment_cash', "Cash Payment")], ondelete={'payment_cash': 'set default'})

    # def _compute_feature_support_fields(self):
    #     """ Override of `payment` to enable additional features. """
    #     super()._compute_feature_support_fields()
    #     self.filtered(lambda p: p.code == 'payment_cash').update({
    #         'support_manual_capture': True,
    #     })

    @api.model
    def _get_compatible_providers(self, *args, currency_id=None, **kwargs):
        """ Override of payment to unlist Cash providers when the currency is not supported. """
        providers = super()._get_compatible_providers(*args, currency_id=currency_id, **kwargs)

        currency = self.env['res.currency'].browse(currency_id).exists()
        if currency and currency.name not in SUPPORTED_CURRENCIES:
            providers = providers.filtered(lambda p: p.code != 'payment_cash')

        return providers

