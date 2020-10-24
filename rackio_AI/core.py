import os, pickle
import pandas as pd
import numpy as np
from rackio_AI._singleton import Singleton
from rackio_AI.managers.preprocess import PreprocessManager
from rackio_AI.rackio_loader.rackio_tpl import TPL
from rackio_AI.managers.data_analysis import DataAnalysisManager
from rackio_AI.preprocessing.synthetic_data import SyntheticData


class RackioAI(Singleton):
    """
    This is the main class of the package.

    **RackioAI** is an open source, MIT License [Rackio-Framework](https://github.com/rack-io/rackio-framework) extension
    to do data analysis (based on [Pandas](https://pandas.pydata.org/)) and deep learning models (based on [Keras](https://keras.io/))
    taking advantage of **Rackio** system architecture.

    You can use it by the following snippet code:
    ```python
    >>> from rackio import Rackio
    >>> from rackio_AI import RackioAI
    >>> app = Rackio()
    >>> RackioAI(app)

    ```
    """

    def __init__(self):
        super(RackioAI, self).__init__()
        self.loader = TPL()
        self.synthetic_data = SyntheticData()
        self._preprocessing_manager = PreprocessManager()
        self._data_analysis_manager = DataAnalysisManager()
        self.app = None

    def __call__(self, app):
        """

        """
        self.app = app

    def load(self, filename):
        """
        You can load data in the following extensions:

        * **.tpl:** Is an [OLGA](https://www.petromehras.com/petroleum-software-directory/production-engineering-software/olga-dynamic-multiphase-flow-simulator)
        extension file.
        * **.pkl:** Numpy arrays or Pandas.DataFrame saved in pickle format.

        **Parameters**

        * **filename:** (str) Complete path with its extension. If the *filename* is a directory, it will load all the files
        with that extension in the directory, and if in the directory there are more directories, it will inspect it to look for more
        files with that extension.

        If the filename is a file with a valid extension, this method will load only that file.

        **return**

        * **data:** (pandas.DataFrame)

        **Example loading a .tpl file**

        ```python
        >>> import os
        >>> from rackio_AI import RackioAI
        >>> from rackio import Rackio
        >>> app = Rackio()
        >>> RackioAI(app)
        >>> cwd = os.getcwd()
        >>> filename = os.path.join(cwd, 'data', 'Leak', 'Leak112.tpl')
        >>> RackioAI.load(filename)
        tag       TIME_SERIES  ...     file
        variable               ... filename
        unit                S  ...     .tpl
        0            0.000000  ...  Leak112
        1            0.502732  ...  Leak112
        2            1.232772  ...  Leak112
        3            1.653696  ...  Leak112
        4            2.200430  ...  Leak112
        ...               ...  ...      ...
        3210      1617.966000  ...  Leak112
        3211      1618.495000  ...  Leak112
        3212      1619.025000  ...  Leak112
        3213      1619.554000  ...  Leak112
        3214      1620.083000  ...  Leak112
        <BLANKLINE>
        [3215 rows x 12 columns]

        **Example loading a .tpl file**

        >>> filename = os.path.join(cwd, 'data', 'Leak')
        >>> RackioAI.load(filename)
        tag       TIME_SERIES  ...     file
        variable               ... filename
        unit                S  ...     .tpl
        0            0.000000  ...  Leak111
        1            0.502732  ...  Leak111
        2            1.232772  ...  Leak111
        3            1.653696  ...  Leak111
        4            2.200430  ...  Leak111
        ...               ...  ...      ...
        32182     1618.124000  ...  Leak120
        32183     1618.662000  ...  Leak120
        32184     1619.200000  ...  Leak120
        32185     1619.737000  ...  Leak120
        32186     1620.275000  ...  Leak120
        <BLANKLINE>
        [32187 rows x 12 columns]

        **Example loading a .pkl with pandas.dataFrame**

        >>> filename = os.path.join(cwd, 'data', 'pkl_files', 'test_data.pkl')
        >>> RackioAI.load(filename)
                    Pipe-60 Totalmassflow_(KG/S)  ...  Pipe-151 Pressure_(PA)
        0.000000                        37.83052  ...                352683.3
        0.502732                        37.83918  ...                353449.8
        1.232772                        37.83237  ...                353587.3
        1.653696                        37.80707  ...                353654.8
        2.200430                        37.76957  ...                353706.8
        ...                                  ...  ...                     ...
        383.031800                     169.36700  ...                374582.2
        383.518200                     169.37650  ...                374575.9
        384.004500                     169.38550  ...                374572.7
        384.490900                     169.39400  ...                374573.0
        384.977200                     169.40170  ...                374576.1
        <BLANKLINE>
        [20000 rows x 4 columns]

        ```
        """
        if os.path.isdir(filename) or os.path.isfile(filename):

            if filename.endswith('.pkl'):
                try:
                    with open(filename, 'rb') as file:
                        data = pickle.load(file)
                except:
                    try:
                        with open(filename, 'rb') as file:
                            data = pd.read_pickle(file)
                    except:
                        raise ImportError('{} is not possible loaded it'.format(filename))

                self.data = data
                return data

            try:
                self._load_data(filename)
                data = self.loader.to('dataframe')
                self._data = data
                return data

            except:
                raise ImportError('{} is not possible loaded because is no a .tpl file'.format(filename))

        else:
            raise TypeError('You can only load .tpl or .pkl files')

    @property
    def data(self):
        """
        Variable where is storaged the loaded data.

        **Parameters**

        None

        **return**

        * **data:** (pandas.DataFrame)
        """
        return self._data

    @data.setter
    def data(self, value):
        """
        value (pd.DataFrame or np.ndarray):
        """
        if isinstance(value, pd.DataFrame) or isinstance(value, np.ndarray):

            if isinstance(value, np.ndarray):
                value = pd.DataFrame(value)

            self.synthetic_data.data = value
        else:
            raise TypeError('value must be a pd.DataFrame or np.ndarray')

        self._data = value

    def append_data(self, data_analysis_object):
        """
        Append a RackioEDA object to the data analysis manager.

        **Parameters**

        * **data_analysis_object:** (RackioEDA): RackioEDA object.

        **return**

        None
        """

        self._data_analysis_manager.append(data_analysis_object)

    def get_data(self, name):
        """
        Returns a RackioEDA object defined by its name.

        **Parameters**

        * **name:** (str) RackioEDA name.

        **return**

        * **data_object:** (RackioEDA) RackioEDA object
        """

        return self._data_analysis_manager.get_data(name)

    def serialize_data(self, name):
        """
        serialize RackioEDA

        **Parameters**

        * **name:** (str) RackioEDA object name

        **return**

        * **data:** (dict) RackioEDA object serialized

        """
        data = self.get_data(name)

        return data.serialize()


    def append_preprocess_model(self, preprocessing_model):
        """
        Append a Preprocessing object to the data analysis manager.

        **Parameters**

        * **preprocessing_model:** (Preprocessing): Preprocessing object.

        **return**

        None
        """

        self._preprocessing_manager.append_preprocessing(preprocessing_model)

    def get_preprocess(self, name):
        """
        Returns a Preprocessing object defined by its name.

        **Parameters**

        * **name:** (str) Preprocessing name.

        **return**

        * **preprocessing_model:** (Preprocesing) Preprocessing model
        """

        return self._preprocess_manager.get_preprocessing_model(name)

    def serialize_preprocess(self, name):
        """
        serialize Preprocessing model

        **Parameters**

        * **name:** (str) Preprocessing model name

        **return**

        * **data:** (dict) Preprocessin model serialized

        """
        preprocess = self.get_preprocess(name)

        return preprocess.serialize()

    def summary(self):
        """
        Get a RackioAI summary.

        **Parameters**

        None

        **return**

        * **result:** (dict) All defined Managers
        """
        result = dict()
        result["preprocessing manager"] = self._preprocess_manager.summary()
        result["data analysis manager"] = self._data_analysis_manager.summary()

        return result

    @staticmethod
    def save_obj(obj, filename, format='pkl'):
        """
        Method to persist any object

        **Parameters**

        * **obj:** (obj) any persistable object
        * **filename:** (str) with no extension
        * **format:** (str) with no dot (.) at the beginning (default='pkl')

        **return**

        * obj in the path defined by *filename*
        """
        if format.lower()=='pkl':

            with open('{}.{}'.format(filename,format), 'wb') as file:
                pickle.dump(obj, file)

    @staticmethod
    def load_obj(filename, format='pkl'):
        """
        load any saved object with RackioAI's save method

        **Parameters**

        * **filename:** (str) with no extension
        * **format:** (str) with no dot (.) at the beginning

        **return**

        * **obj:** (obj)
        """
        obj = None
        if format.lower()=='pkl':

            with open('{}.{}'.format(filename,format), 'rb') as file:
                obj = pickle.load(file)

        return obj

    def load_test_data(self, *name):
        """
        Load RackioAI test data contained in folder data

        rackio_AI package has a folder called data

        > rackio_AI/data

        In this directory there are the following folders

        > rackio_AI/data/Leak
        > rackio_AI/data/pkl_files

        *test_data* allows to you an specific file or all files in the previous folders

        **Parameters**

        * **name:** (str) a folder name or filename in rackio_AI/data

        **return**

        * **data:** (pandas.DataFrame)

        #**Example**

        ```python
        >>> from rackio_AI import RackioAI
        >>> from rackio import Rackio
        >>> app = Rackio()
        >>> RackioAI(app)
        >>> RackioAI.load_test_data('Leak') # Load test data fron a folder
        tag       TIME_SERIES  ...     file
        variable               ... filename
        unit                S  ...     .tpl
        0            0.000000  ...  Leak111
        1            0.502732  ...  Leak111
        2            1.232772  ...  Leak111
        3            1.653696  ...  Leak111
        4            2.200430  ...  Leak111
        ...               ...  ...      ...
        32182     1618.124000  ...  Leak120
        32183     1618.662000  ...  Leak120
        32184     1619.200000  ...  Leak120
        32185     1619.737000  ...  Leak120
        32186     1620.275000  ...  Leak120
        <BLANKLINE>
        [32187 rows x 12 columns]
        >>> RackioAI.load_test_data('Leak', 'Leak111.tpl') # Load test data from a file in Leak Folder
        tag       TIME_SERIES  ...     file
        variable               ... filename
        unit                S  ...     .tpl
        0            0.000000  ...  Leak111
        1            0.502732  ...  Leak111
        2            1.232772  ...  Leak111
        3            1.653696  ...  Leak111
        4            2.200430  ...  Leak111
        ...               ...  ...      ...
        3214      1618.327000  ...  Leak111
        3215      1618.849000  ...  Leak111
        3216      1619.370000  ...  Leak111
        3217      1619.892000  ...  Leak111
        3218      1620.413000  ...  Leak111
        <BLANKLINE>
        [3219 rows x 12 columns]

        ```
        """
        if not os.getcwd().split(os.path.sep)[-1]=='RackioAI':
            os.chdir('..')

        cwd = os.getcwd()
        filename = os.path.join(cwd, 'rackio_AI', 'data', *name)
        self._load_data(filename)
        data = self.loader.to('dataframe')

        return data

    def _load_data(self, filename):
        """

        """
        return self.loader.read(filename)

if __name__=="__main__":
    import doctest
    doctest.testmod()