
import KeepAnEyeOn as kaeo
import PatternRecog as pr


# starting working on keepAnEyeOn(KAEO) sheet:
keepeye = kaeo.KeepAnEyeOn()
keepeye.kaeoWorker()

print('done with KeeyAnEyeOn sheet, start checking todays patterns for stocks')

# starting working on Pattern Recognition
Pattern = pr.PatternRecog()
Pattern.PatternRecogWorker()

print('all done!!!')



# todo: Trade simulation script to simlulate if I bought the symbol, and what is outcome everyday afterward.
# todo: complete the code for CEO-BUYS -- get the data and check the price and volumn, and put it on the KAEO sheet
# todo: delete the old files in output folder?
# todo: make the number of days in excel file configurable, current is 10 days.
# todo: ip addrs proxy?
# todo: fetch index symbols list from website
