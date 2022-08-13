
import os

from deals_lib import deals

dir_name = os.path.basename(__file__)

dealUrl= "https://api.pipe.run/v1/deals?updated_at_start={} 00:00:00&with=users&show=50&page={}"


main = deals().main(dealUrl,dir_name,up='up')
print(main)