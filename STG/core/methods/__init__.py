from core.methods.jaro import Jaro
from core.methods.jaccard import Jaccard
from core.methods.sorensen import Sorensen
from core.methods.jaro_winkler import JaroWinkler

from core.methods.interface import Method

__version__ = 1.0

__all__ = [
    'Jaro',
    'Jaccard',
    'Sorensen',
    'JaroWinkler',
    'Method'
]
