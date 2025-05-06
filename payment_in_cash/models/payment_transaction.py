from odoo import fields, models, api, _

from odoo.addons.payment_in_cash.const import PAYMENT_STATUS_MAPPING
from ..controllers.controllers import CashPaymentController
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):   # Poner el currency??
        """ Override of payment to return cash-specific rendering values.
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payment_cash':
            return res

        processing_values.update({
            'api_url': CashPaymentController._accept_url,
            'currency_id' : self.currency_id,
            'partner_id': self.partner_id,
            'amount': self.amount,
            'currency_code': self.currency_id.name,
            'provider_code': self.provider_code,
            'provider_id': self.provider_id,
            'reference': self.reference
        })

        return processing_values

    @api.model
    def _get_tx_from_notification_data(self, provider, data):
        """ Override of payment to find the transaction.
        """
        tx = super()._get_tx_from_notification_data(provider, data)
        if provider != 'payment_cash':
            return tx

        reference = data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'payment_cash')])
        if not tx:
            raise ValidationError(
                "Cash Transaction: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, data):
        """ Override of payment to process the transaction based.

        Note: self.ensure_one()

        :param dict data: The feedback data sent by the provider
        :return: None
        :raise: ValidationError if inconsistent data were received
        """
        if (len(self._ids) > 0):
            super()._process_notification_data(data)
        if self.provider_code != 'payment_cash':
            return

        if 'payment_status' in data:
            payment_status = data.get('payment_status')

            if payment_status in PAYMENT_STATUS_MAPPING['pending']:
                self._set_pending()  # self._set_pending(state_message=data.get('pending_reason'))
            elif payment_status in PAYMENT_STATUS_MAPPING['done']:
                self._set_done()
            elif payment_status in PAYMENT_STATUS_MAPPING['cancel']:
                self._set_canceled()
            else:
                _logger.info(
                    "received data with invalid payment status (%s) for transaction with reference %s",
                    payment_status, self.reference
                )
                self._set_error(
                    "Cash: " + _("Received data with invalid payment status: %s", payment_status)
                )

    def _get_post_processing_values(self):
        """ Return a dict of values used to display the status of the transaction.

        For an acquirer to handle transaction status display, it must override this method and
        return a dict of values. Acquirer-specific values take precedence over those of the dict of
        generic post-processing values.

        The returned dict contains the following entries:
            - provider: The provider of the acquirer
            - reference: The reference of the transaction
            - amount: The rounded amount of the transaction
            - currency_id: The currency of the transaction, as a res.currency id
            - state: The transaction state: draft, pending, authorized, done, cancel or error
            - state_message: The information message about the state
            - is_post_processed: Whether the transaction has already been post-processed
            - landing_route: The route the user is redirected to after the transaction
            - Additional acquirer-specific entries

        Note: self.ensure_one()

        :return: The dict of processing values
        :rtype: dict
        """
        post_processing_values = super()._get_post_processing_values()
        post_processing_values.update({"id": self.id})

        return post_processing_values
