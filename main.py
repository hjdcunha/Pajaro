import pajaro
import sys
from Configuration.configuration import Configuration
from Database.database import PajaroDatabase

bot = pajaro.Pajaro(sys.argv[1], sys.argv[2])

while True:
    bot.run()