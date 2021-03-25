from scipy.stats import kurtosis, skew
from rackio_AI.utils.utils_core import Utils
import pywt
import numpy as np
from easy_deco.del_temp_attr import set_to_methods, del_temp_attr


@set_to_methods(del_temp_attr)
class StatisticalsFeatures:
    """
    Documentation here
    """
    _instances = list()

    def __init__(self):
        pass

    def mean(
        self, 
        dataset,
        axis=None,
        dtype=None,
        out=None,
        keepdims=np._NoValue
        ):
        r"""
        Compute the arithmetic mean along the specified axis.
        Returns the average of the array elements.  The average is taken over
        the flattened array by default, otherwise over the specified axis.
        `float64` intermediate and return values are used for integer inputs.
        
        **Parameters**
        
        * **dataset:** (2d array_like) Array containing numbers whose mean is desired. If `a` is not an
        array, a conversion is attempted.
        * **axis:** (None or int or tuple of ints, optional) Axis or axes along which the means are computed. 
        The default is to compute the mean of the flattened array.
        If this is a tuple of ints, a mean is performed over multiple axes, instead of a single axis or all the
        axes as before.
        * **dtype:** (data-type, optional) Type to use in computing the mean.  For integer inputs, the default
        is `float64`; for floating point inputs, it is the same as the input dtype.
        * **out:** (ndarray, optional) Alternate output array in which to place the result.  The default
        is ``None``; if provided, it must have the same shape as the expected output, but the type will be cast if
        necessary.
        * **keepdims:** (bool, optional) If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option, the result will broadcast correctly against the 
        input array. If the default value is passed, then `keepdims` will not be passed through to the `mean` method 
        of sub-classes of `ndarray`, however any non-default value will be.  If the sub-class' method does not implement
        `keepdims` any exceptions will be raised.
        
        **Returns**
        
        * **m:** (ndarray, see dtype parameter above) If `out=None`, returns a new array containing the mean values,
        otherwise a reference to the output array is returned.

        ## Snippet code

        ```python
        >>> from rackio_AI import RackioAIFE
        >>> feature_extraction = RackioAIFE()
        >>> dataset = np.array([[1, 2], [3, 4]])
        >>> feature_extraction.stats.mean(dataset)
        2.5
        >>> feature_extraction.stats.mean(dataset, axis=0)
        array([2., 3.])
        >>> feature_extraction.stats.mean(dataset, axis=1)
        array([1.5, 3.5])

        ```
        """
        dataset = Utils.check_dataset_shape(dataset)
        _mean = np.mean(dataset, axis=axis, dtype=dtype, out=out, keepdims=keepdims)

        return _mean

    def median(
        self, 
        dataset, 
        axis=None, 
        out=None, 
        overwrite_input=False, 
        keepdims=False
        ):
        r"""
        Compute the median along the specified axis.
        Returns the median of the array elements.
        
        **Parameters**
        
        * **dataset:** (2d array_like) Input array or object that can be converted to an array.
        * **axis:** ({int, sequence of int, None}, optional) Axis or axes along which the medians \
        are computed. The default is to compute the median along a flattened version of the array.
        * **out:** (ndarray, optional) Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output, but the type (of the output) 
        will be cast if necessary.
        * **overwrite_input:** (bool, optional) If True, then allow use of memory of input array 
        `dataset` for calculations. The input array will be modified by the call to `median`. 
        This will save memory when you do not need to preserve the contents of the input array. 
        Treat the input as undefined, but it will probably be fully or partially sorted. Default is
        False. If `overwrite_input` is ``True`` and `dataset` is not already an `ndarray`, an error
        will be raised.
        * **keepdims:** (bool, optional) If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option, the result will broadcast 
        correctly against the original `arr`.
        
        **Returns**
        
        * **median:** (ndarray) A new array holding the result. If the input contains integers
        or floats smaller than ``float64``, then the output data-type is ``np.float64``.  
        Otherwise, the data-type of the output is the same as that of the input. If `out` is 
        specified, that array is returned instead.

        ## Notes
        
        Given a vector $V$ of length $N$, the median of $V$ is the
        middle value of a sorted copy of $V$, $V_{sorted}$ - i
        e., ``V_sorted[(N-1)/2]``, when $N$ is odd, and the average of the
        two middle values of ``V_sorted`` when ``N`` is even.
        
        ## Snippet code
        
        ```python
        >>> from rackio_AI import RackioAIFE
        >>> feature_extraction = RackioAIFE()
        >>> dataset = np.array([[10, 7, 4], [3, 2, 1]])
        >>> feature_extraction.stats.median(dataset)
        3.5
        >>> feature_extraction.stats.median(dataset, axis=0)
        array([6.5, 4.5, 2.5])
        >>> feature_extraction.stats.median(dataset, axis=1)
        array([7., 2.])
        >>> m = feature_extraction.stats.median(dataset, axis=0)
        >>> out = np.zeros_like(m)
        >>> feature_extraction.stats.median(dataset, axis=0, out=m)
        array([6.5, 4.5, 2.5])
        >>> m
        array([6.5, 4.5, 2.5])
        >>> b = dataset.copy()
        >>> feature_extraction.stats.median(b, axis=1, overwrite_input=True)
        array([7., 2.])
        >>> assert not np.all(dataset==b)
        >>> b = dataset.copy()
        >>> feature_extraction.stats.median(b, axis=None, overwrite_input=True)
        3.5
        >>> assert not np.all(dataset==b)

        ```
        """
        dataset = Utils.check_dataset_shape(dataset)
        _median = np.median(dataset, axis=axis, out=out, overwrite_input=overwrite_input, keepdims=keepdims)

        return _median

    def kurt(
        self, 
        dataset, 
        axis: int=0, 
        fisher: bool=True, 
        bias: bool=True, 
        nan_policy: str='propagate'
        ):
        r"""
        Compute the kurtosis (Fisher or Pearson) of a dataset

        Kurtosis is the fourth central moment divided by the square of the variance. If Fisher's definiton
        is used, then 3.0 is subtracted from the result to give 0.0 for a normal distribution.

        If bias is False then the kurtosis is calculated using k statistics to eliminate bias coming from
        biased moment estimators

        **Parameters**

        * **dataset:** (2d array) Data for which the kurtosis is calculated
        * **axis:** (int or None) Axis along which the kurtosis is calculated. Default is 0. If None, compute
        over the whole array dataset.
        * **fisher:** (bool) If True, Fisher's definition is used (normal ==> 0.0). If False, Pearson's deifnition
        is used (normal ==> 3.0)
        * **bias:** (bool) If False, then the calculations are corrected for statistical bias.
        * **nan_policy:** ({'propagate', 'raise', 'omit'}) Defines how to handle when inputs contains nan. 'propagate' 
        returns nan, 'raise' throws an error, 'omit' performs the calculations ignoring nan values. Default is propagate.

        **returns**

        * **kurtosis** (array 1xcols_dataset) The kurtosis of values along an axis. If all values are equal, return -3 for Fisher's definition
        and 0 for Pearson's definition

        ## Snippet Code
        ```python
        >>> from scipy.stats import norm
        >>> from rackio_AI import RackioAIFE
        >>> feature_extraction = RackioAIFE()
        >>> dataset = norm.rvs(size=1000, random_state=3)
        >>> feature_extraction.stats.kurt(dataset)
        array([-0.06928694])

        ```

        ## Snippet Code
        ```python
        >>> from scipy.stats import norm
        >>> from rackio_AI import RackioAIFE
        >>> feature_extraction = RackioAIFE()
        >>> dataset = norm.rvs(size=(1000,2), random_state=3)
        >>> feature_extraction.stats.kurt(dataset)
        array([-0.00560946, -0.1115389 ])

        ```
        """
        dataset = Utils.check_dataset_shape(dataset)
        _, cols = dataset.shape
        _kurt = np.array([kurtosis(
            dataset[:, col], 
            axis=axis, 
            fisher=fisher, 
            bias=bias, 
            nan_policy=nan_policy
            ) for col in range(cols)]
        )

        return _kurt

    def std(
        self, 
        dataset, 
        axis=None,
        dtype=None,
        out=None,
        ddof=0,
        keepdims=np._NoValue
        ):
        r"""
        Compute the standard deviation along the specified axis.

        Returns the standard deviation, a measure of the spread of a distribution,
        of the array elements. The standard deviation is computed for the
        flattened array by default, otherwise over the specified axis.
        
        **Parameters**
        
        * **dataset:** (2d array_like) Calculate the standard deviation of these values.
        * **axis:** (None or int or tuple of ints, optional) Axis or axes along which the standard deviation is computed.
        The default is to compute the standard deviation of the flattened array.
        If this is a tuple of ints, a standard deviation is performed over multiple axes, instead of a single
        axis or all the axes as before.
        * **dtype:** (dtype, optional) Type to use in computing the standard deviation. For arrays of
        integer type the default is float64, for arrays of float types it is the same as the array type.
        * **out:** (ndarray, optional) Alternative output array in which to place the result. It must have
        the same shape as the expected output but the type (of the calculated values) will be cast if necessary.
        * **ddof:** (int, optional) Means Delta Degrees of Freedom.  The divisor used in calculations
        is $N - ddof$, where $N$ represents the number of elements. By default `ddof` is zero.
        * **keepdims:** (bool, optional) If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option, the result will broadcast correctly 
        against the input array. If the default value is passed, then `keepdims` will not be passed through 
        to the `std` method of sub-classes of `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any exceptions will be raised.

        **Returns**
        
        * **standard_deviation:** (ndarray) If `out` is None, return a new array containing the standard deviation,
        otherwise return a reference to the output array.

        ## Notes
        
        The standard deviation is the square root of the average of the squared
        deviations from the mean, i.e.

        $\mu = \frac{1}{N}\sum_{i=1}^{n}dataset_{i}$

        $std = \sqrt{\frac{1}{N}\sum_{i=1}^{n}|dataset_{i}-\mu|^2}$
        
        ## Snippet code
        ```python
        >>> import numpy as np
        >>> from rackio_AI import RackioAIFE
        >>> feature_extraction = RackioAIFE()
        >>> dataset = np.array([[1, 2], [3, 4]])
        >>> feature_extraction.stats.std(dataset, axis=0)
        array([1., 1.])
        >>> feature_extraction.stats.std(dataset, axis=1)
        array([0.5, 0.5])

        ```
        
        ### In single precision, std() can be inaccurate

        ```python
        >>> dataset = np.zeros((2, 512*512), dtype=np.float32)
        >>> dataset[0, :] = 1.0
        >>> dataset[1, :] = 0.1
        >>> feature_extraction.stats.std(dataset)
        0.45000005
        >>> dataset = np.array([[14, 8, 11, 10], [7, 9, 10, 11], [10, 15, 5, 10]])
        >>> feature_extraction.stats.std(dataset)
        2.614064523559687

        ```
        """
        dataset = Utils.check_dataset_shape(dataset)
        _std = np.std(dataset, axis=axis, dtype=dtype, out=dtype, ddof=ddof, keepdims=keepdims)
        return _std

    def skew(
        self, 
        dataset, 
        axis=0,
        bias=True,
        nan_policy='propagate'
        ):
        r"""
        Compute the sample skewness of a data set.
        For normally distributed data, the skewness should be about zero. For
        unimodal continuous distributions, a skewness value greater than zero means
        that there is more weight in the right tail of the distribution. The
        function `skewtest` can be used to determine if the skewness value
        is close enough to zero, statistically speaking.
        
        **Parameters**

        * **dataset:** (ndarray) Input array.
        * **axis:** (int or None, optional) Axis along which skewness is calculated. Default is 0.
        If None, compute over the whole array `a`.
        * **bias:** (bool, optional) If False, then the calculations are corrected for statistical bias.
        * **nan_policy:** ({'propagate', 'raise', 'omit'}, optional) Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):
            * 'propagate': returns nan
            * 'raise': throws an error
            * 'omit': performs the calculations ignoring nan values
        
        **Returns**
        
        * **skewness:** (ndarray) The skewness of values along an axis, returning 0 where all values are equal.
        
        ## Notes

        The sample skewness is computed as the Fisher-Pearson coefficient
        of skewness, i.e.

        $g_1=\frac{m_3}{m_2^{3/2}}$

        where

        $m_i=\frac{1}{N}\sum_{n=1}^N(x[n]-\bar{x})^i$
        
        is the biased sample $i\texttt{th}$ central moment, and $\bar{x}$ is
        the sample mean.  If $bias$ is False, the calculations are
        corrected for bias and the value computed is the adjusted
        Fisher-Pearson standardized moment coefficient, i.e.

        $G_1=\frac{k_3}{k_2^{3/2}}=\frac{\sqrt{N(N-1)}}{N-2}\frac{m_3}{m_2^{3/2}}.$
        
        ## References
        
        .. [1] Zwillinger, D. and Kokoska, S. (2000). CRC Standard
        Probability and Statistics Tables and Formulae. Chapman & Hall: New
        York. 2000.
        Section 2.2.24.1
        
        ## Snippet code
        ```python
        >>> import numpy as np
        >>> from rackio_AI import RackioAIFE
        >>> feature_extraction = RackioAIFE()
        >>> dataset = np.array([1, 2, 3, 4, 5])
        >>> feature_extraction.stats.skew(dataset)
        array([0.])
        >>> dataset = np.array([2, 8, 0, 4, 1, 9, 9, 0])
        >>> feature_extraction.stats.skew(dataset)
        array([0.26505541])
        
        ```
        """
        dataset = Utils.check_dataset_shape(dataset)
        _, cols = dataset.shape
        _skew = np.array([skew(
            dataset[:, col], 
            axis=axis, 
            bias=bias, 
            nan_policy=nan_policy
            ) for col in range(cols)]
        )
        return _skew

    def rms(self, dataset):
        r"""
        One of the most important basic features that can be extracted directly from the time-domain
        signal is the RMS which describe the energy of the signal. It is defined as the square root
        of the average squared value of the signal and can also be called the normalized energy of the
        signal.

        $RMS = \sqrt{\frac{1}{n}\sum_{i=0}^{n-1}S_{i}^{2}}$
        
        Especially in vibration analysis the RMS is used to perform fault detection, i.e. triggering an
        alarm, whenever the RMS surpasses a level that depends on the size of the machine, the nature
        of the signal (for instance velocity or acceleration), the position of the accelerometer, and so on.
        After the detection of the existence of a failure, fault diagnosis is performed relying on more
        sophisticated features. For instance the ISO 2372 (VDI 2056) norms define three different velocity
        RMS alarm levels for four different machine classes divided by power and foundations of the rotating
        machines.

        **Parameters**

        * **dataset:** (2d array)

        **Returns**

        """
        _rms = np.array([(np.sum(col ** 2, axis=0) / dataset.shape[0]) ** 0.5 for col in dataset])
        return _rms

    def peak_2_valley(self, dataset, axis=0):
        r"""
        Another important measurement of a signal, considering a semantically coeherent sampling
        interval, for instance a fixed-length interval or one period of a rotation, is the peak-to-valley
        (PV) value which reflects the amplitude spread of a signal:

        $PV=\frac{1}{2}\left(\max{dataset}\quad -\quad \min{dataset}\right)$
        """
        _peak_2_valley = np.array([(np.max(col, axis=axis)-np.min(col, axis=axis)) / 2 for col in data])

        return _peak_2_valley

    def peak(self, dataset, ref=None, axis=0, rate=None, **kwargs):
        r"""
        I we consider only the maximum amplitude relative to zero $s_{ref}=0$ or a general reference
        level $s_{ref}$, we get the peak value

        $peak = \max\left(dataset_{i}-ref\right)$

        Often the peak is used in conjunction with other statistical parameters, for instance the 
        peak-to-average rate.

        $peak = \frac{\max\left(dataset_{i}-ref\right)}{\frc{1}{N}\sum_{i=0}^{N-1}dataset_{i}}$

        or peak-to-median rate

        """
        if ref not None:

            _peak = np.array([np.max(col - ref, axis=axis) for col in data])

        else:
            
            _peak = np.array([np.max(col - col[0,:], axis=axis) for col in data])

        if rate not None:

            if rate.lower() == 'average':
                
                return _peak / self.mean(dataset, **kwargs

            elif rate.lower() == 'median':

                return _peak / self.median(dataset, **kwargs)

        else:
            
            return _peak
            
    def crest_factor(self):
        """Documentation here"""
        peak = self.peak()
        rms = self.rms()
        return np.array([peak[i,:] / rms[i,:] for i in range(peak.shape[0])])

    def __call__(
        self, 
        dataset, 
        std=True, 
        mean=False,
        rms=False,
        kurt=False,
        skew=False,
        peak=False,
        peak_2_valley=False,
        crest_factor=False,
        concatenate=True
        ):
        """
        Documentation here
        """
        result = list()
        features = {
            'std': std,
            'mean': mean,
            'rms': rms, 
            'kurt': kurt, 
            'skew': skew, 
            'peak': peak, 
            'peak_2_valley': peak_2_valley, 
            'crest_factor': crest_factor
        }

        for key, value in features.items():
            
            if value:
                feature = getattr(self, key)
                result.append(feature(data))

        if concatenate:

            result = np.concatenate(result, axis=1)

        return result


@set_to_methods(del_temp_attr)
class FrequencyFeatures:
    """
    Documentation here
    """
    _instances = list()

    def __init__(self):
        pass

    def wavelets(self, _type='db2', lvl=3):
        """
        Documentation here
        """
        waveletFeatures = list()
        lastCoeffs = 3
        for data in self.inputData:
            coeffs = pywt.wavedec(data, _type, level=lvl, axis=0)
            waveletFeatures.append(np.concatenate([sum(coeff ** 2, 0) for coeff in coeffs[0:lastCoeffs]],axis=0))
        return np.array(waveletFeatures)

    def __call__(self, *args, **kwargs):
        """
        Documentation here
        """
        pass


@set_to_methods(del_temp_attr)
class RackioAIFE:
    """
    Documentation here
    """
    _instances = list()
    

    def __init__(self):
        """
        Documentation here
        """
        self.stats = StatisticalsFeatures()
        self.frequency_domain = FrequencyFeatures()


if __name__=='__main__':

    import doctest

    doctest.testmod()