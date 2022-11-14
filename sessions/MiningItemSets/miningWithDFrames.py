from pyspark.sql import *
from pyspark.sql.functions import array_contains,array,col,collect_list,udf
 from pyspark.sql.types import ArrayType,IntegerType


t3 = Row( id=3, tr=[9,10,11,12] )
t2 = Row( id=2, tr=[5,6,7,8] )
t1 = Row( id=1, tr=[1,2,3,4] )
df1 = spark.createDataFrame( [t1,t2,t3] )

fi1 = Row( it=2, fr=4 )
fi2 = Row( it=4, fr=6 )
fi3 = Row( it=6, fr=6 )
fi4 = Row( it=8, fr=8 )
fi6 = Row( it=10, fr=8 )
fi5 = Row( it=10, fr=8 )
fi6 = Row( it=12, fr=8 )
df2 = spark.createDataFrame( [fi1,fi2,fi3,fi4,fi5,fi6] )
display(df1)

joined = df1.join(df2, array_contains(df1.tr,df2.it) )
joined.show()
 +---+---------------+---+---+
 | id|             tr| it| fr|
 +---+---------------+---+---+
 |  1|   [1, 2, 3, 4]|  2|  4|
 |  1|   [1, 2, 3, 4]|  4|  6|
 |  2|   [5, 6, 7, 8]|  6|  6|
 |  2|   [5, 6, 7, 8]|  8|  8|
 |  3|[9, 10, 11, 12]| 10|  8|
 |  3|[9, 10, 11, 12]| 12|  8|
 +---+---------------+---+---+

reduced = joined.groupBy("tr")

aggregated = reduced.agg(collect_list("it"))

aggregated.show()
 +---------------+----------------+                                              
 |             tr|collect_list(it)|
 +---------------+----------------+
 |[9, 10, 11, 12]|        [10, 12]|
 |   [5, 6, 7, 8]|          [6, 8]|
 |   [1, 2, 3, 4]|          [2, 4]|
 +---------------+----------------+

# Finally, filterout elements not in L_1 (df2):

def filteroutElements(l,flist):
   return [it for it in l if it in flist]

filterout_udf = udf( lambda l,flist : filteroutElements(l,flist), ArrayType(IntegerType()) )

# Info about UDF functions : https://changhsinlee.com/pyspark-udf/
#
#filtered = aggregated.transform( lambda idf : idf.select([filterout_udf(col("tr"),col("collect_list(it)"))]) )
filtered = aggregated.select(  [ filterout_udf('tr','collect_list(it)') ] )

