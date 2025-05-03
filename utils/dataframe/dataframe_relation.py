import pandas as pd
from dataclasses import dataclass

@dataclass
class DataframeRelation:
    """
    A class to manage relationships between two pandas DataFrames based on specified keys and queries.
    Attributes
    ----------
    left_dataframe : pd.DataFrame
        The left DataFrame to be used in the relationship.
    left_key : str
        The column name in the left DataFrame to be used as the key for the relationship.
    right_dataframe : pd.DataFrame
        The right DataFrame to be used in the relationship.
    right_key : str
        The column name in the right DataFrame to be used as the key for the relationship.
    query : str, optional
        A query string to filter the left DataFrame (default is an empty string).
    Methods
    -------
    __post_init__()
        Validates that the specified keys exist in their respective DataFrames.
    _query_dataframe() -> pd.DataFrame
        Returns the result of applying the query to the left DataFrame.
    _get_filtered_left_dataframe() -> pd.Series
        Retrieves the filtered left DataFrame's key column based on the query.
    _get_filtered_right_dataframe() -> pd.DataFrame
        Filters the right DataFrame based on the keys from the filtered left DataFrame.
    search(query: str) -> pd.DataFrame
        Executes the query on the left DataFrame and returns the merged result with the right DataFrame.
    """
    left_dataframe: pd.DataFrame
    left_key: str
    right_dataframe: pd.DataFrame
    right_key: str
    query: str = ""

    def __post_init__(self):
        if self.left_key not in self.left_dataframe.columns:
            raise ValueError(f"Key '{self.left_key}' not found in left dataframe columns.")
        if self.right_key not in self.right_dataframe.columns:
            raise ValueError(f"Key '{self.right_key}' not found in right dataframe columns.")

    def _query_dataframe(self) -> pd.DataFrame:
        """Returns the result of the query on the left dataframe."""
        if not self.query:
            return self.left_dataframe
        return self.left_dataframe.query(self.query)

    def _get_filtered_left_dataframe(self) -> pd.Series:
        """
        Filters the left dataframe based on a query and retrieves a specific column.
        This method applies a query to filter the left dataframe and returns the 
        values of the column specified by `self.left_key`. If the query results 
        in an empty dataframe, a ValueError is raised.
        Returns:
            pd.Series: A pandas Series containing the values of the column 
            specified by `self.left_key` from the filtered dataframe.
        Raises:
            ValueError: If the query results in an empty dataframe.
        """
        filtered_left_df = self._query_dataframe()

        if filtered_left_df.empty:
            raise ValueError("The query returned an empty dataframe.")

        return filtered_left_df[self.left_key]

    def _get_filtered_right_dataframe(self) -> pd.DataFrame:
        """
        Filters the right DataFrame based on the keys present in the filtered left DataFrame.

        This method retrieves the filtered left DataFrame keys and uses them to filter
        the rows in the right DataFrame where the values in the specified right key column
        match the keys from the left DataFrame.

        Returns:
            pd.DataFrame: A filtered DataFrame containing rows from the right DataFrame
            that match the keys from the filtered left DataFrame.
        """
        left_keys = self._get_filtered_left_dataframe()
        return self.right_dataframe[self.right_dataframe[self.right_key].isin(left_keys)]

    def search(self, query: str) -> pd.DataFrame:
        """
        Executes the provided query on the dataframes and returns the merged result.
        Args:
            query (str): The query string to filter the dataframes.
        Returns:
            pd.DataFrame: A merged dataframe resulting from applying the query to the left
            and right dataframes and merging them based on the specified keys.
        """
        self.query = query
        filtered_left_df = self._query_dataframe()
        filtered_right_df = self._get_filtered_right_dataframe()

        return filtered_left_df.merge(filtered_right_df, left_on=self.left_key, right_on=self.right_key)
