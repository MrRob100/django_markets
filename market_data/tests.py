from django.test import TestCase
from django.urls import reverse
from .models import Candle

STOCK_SYMBOL_TEST='MSFT'
CRYPTO_SYMBOL_TEST='DOT'
FOREX_PAIR_TEST='EURGBP'

CREATE_STOCK_DATA_URL = reverse('stock_candles', kwargs={'symbol': STOCK_SYMBOL_TEST})
CREATE_CRYPTO_DATA_URL = reverse('crypto_candles', kwargs={'symbol': CRYPTO_SYMBOL_TEST})
CREATE_FOREX_DATA_URL = reverse('forex_candles', kwargs={'pair': FOREX_PAIR_TEST})


class PublicUserApiTests(TestCase):
    """Test the market data database caching behaviour is correct"""

    def test_stock_data_works(self):
        res = self.client.get(CREATE_STOCK_DATA_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Candle.objects.filter(asset_class='stock', symbol=STOCK_SYMBOL_TEST).exists())

    def test_crypto_data_works(self):
        res = self.client.get(CREATE_CRYPTO_DATA_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Candle.objects.filter(asset_class='crypto', symbol=CRYPTO_SYMBOL_TEST).exists())

    def test_forex_data_works(self):
        res = self.client.get(CREATE_FOREX_DATA_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Candle.objects.filter(asset_class='crypto', symbol=FOREX_PAIR_TEST).exists())