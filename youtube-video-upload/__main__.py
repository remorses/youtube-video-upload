import sys
import yaml
import json
import traceback
from .upload_from_options import upload_from_options
from colorama import init, Fore


try:
    yaml_file = open(sys.argv[-1], 'r+')
    options = yaml.load(yaml_file.read())
    new_options = upload_from_options(options)
    yaml_file.close()
except KeyboardInterrupt:
    pass
except Exception as e:
    init(autoreset=True)
    print()
    print(Fore.RED + traceback.format_exc())
finally:
    print()
    yaml_file.close()




# yaml_file.seek(0)
# yaml_file.write(yaml.dump(
#         new_options,
#         indent=4,)
#     )
# yaml_file.truncate()
