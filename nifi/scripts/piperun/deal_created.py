
import os

from deals_lib import deals

dir_name = os.path.basename(__file__)

dealUrl = "https://api.pipe.run/v1/deals?created_at_start={}&with=users&show=50&page={}"


main = deals().main(dealUrl,dir_name)
print(main)