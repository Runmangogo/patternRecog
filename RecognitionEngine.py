import datetime as dt
import numpy as np

class RecognitionEngine:

    def __init__(self):
        pass

    # go over different time span
    def timespansChecker(self, index, symbol, open_price, close_price, high_price, low_price):

        length = open_price.__len__()
        endidx = length - 1
        todayhigh = high_price[-1]
        wl = symbol + '|'
        ha = symbol + '|'

        # if there is element with 'null' value in lists, we need to remove it from them.
        if open_price.count(None) > 0:
            print('found None value in the open_price')
            wl = wl + '*'
            ha = ha + '*'
            open_price = list(filter(lambda x: x is not None, open_price))
            close_price = list(filter(lambda x: x is not None, close_price))
            high_price = list(filter(lambda x: x is not None, high_price))
            low_price = list(filter(lambda x: x is not None, low_price))

        # put this info in the dict with key is startind and value is timerange
        startidx = {}
        # 365 - 10 holidays : avg 21 weekdays per month
        # 4 months
        startidx[endidx - 83] = '4m'
        # 5 months
        startidx[endidx - 104] = '5m'
        startidx[endidx - 125] = '6m'
        startidx[endidx - 146] = '7m'
        startidx[endidx - 167] = '8m'
        startidx[endidx - 188] = '9m'
        startidx[endidx - 209] = '10m'
        startidx[endidx - 230] = '11m'
        startidx[endidx - 250] = '12m'
        startidx[endidx - 292] = '14m'
        startidx[endidx - 334] = '16m'
        startidx[endidx - 375] = '18m'
        startidx[endidx - 417] = '20m'
        startidx[endidx - 459] = '22m'
        # 12 months
        startidx[0] = '24m'

        for eachKey in startidx.keys():

            # do this check, to make sure there is no minus value for start index
            if eachKey >= 0:
                try:
                    # (endidx-1), we should exclude the current day, so we can work out alert list.
                    open_pricet = open_price[eachKey:(endidx-1)]
                    close_pricet = close_price[eachKey:(endidx-1)]
                    high_pricet = high_price[eachKey:(endidx-1)]
                    low_pricet = low_price[eachKey:(endidx-1)]
                    period = startidx[eachKey]

                    in_list = self.priceTunnelChecker(open_pricet, close_pricet, high_pricet, low_pricet, todayhigh)

                    if in_list == 1:
                        ha = ha + '_' + period
                    if in_list == 2:
                        wl = wl + '_' + period
                    if in_list == 3:
                        ha = ha + '_' + period
                        wl = wl + '_' + period
                except Exception as e:
                    print('timespansChecker: error in ' + startidx[eachKey] + '\n')
                    print(e)


        try:

            if ha.__len__() > symbol.__len__() + 2:
                f_ha = open('C:\\MyProjects\\output\\' + dt.date.today().isoformat() + '_' + index + '_HighAlert' + '.txt', 'a')
                f_ha.write(ha+'\n')
                f_ha.close()

            if wl.__len__() > symbol.__len__() + 2:
                f_wl = open('C:\\MyProjects\\output\\' + dt.date.today().isoformat() + '_' + index + '_WatchList' + '.txt', 'a')
                f_wl.write(wl+'\n')
                f_wl.close()
        except Exception as e:
            print('timespansChecker: ')
            print(e)

    # watch_List/high_Alert_List
    def priceTunnelChecker(self, open_pricet, close_pricet, high_pricet, low_pricet, todayhigh):

        # 0x00 = 0: not in watchList not in HighAlert
        # 0x01 = 1: not in watchList     in HighAlert
        # 0x10 = 2:     in watchList not in HighAlert
        # 0x11 = 3:     in watchList     in HighAlert
        in_list = 0

        # Ajust below parameters to get the better pattern I want to get.
        pricerange_bias = 0.15
        dayrange_bias = 0.076  # (1/12 (or 1/13? 1/14)
        RequiredValidHighLandmarks_ha = 3
        RequiredValidHighLandmarks_wl = 4
        RequiredValidLowLandmarks_ha = 2
        RequiredValidLowLandmarks_wl = 2

        try:
            maxopen = max(open_pricet)
            minopen = min(open_pricet)
            maxclose = max(close_pricet)
            minclose = min(close_pricet)
            maxhigh = max(high_pricet)
            minhigh = min(high_pricet)
            maxlow = max(low_pricet)
            minlow = min(low_pricet)

            price_range = max(maxopen, maxclose) - min(minopen, minclose)
            date_range = open_pricet.__len__()

            # to find out the indices of all occurrences of same price
            allhighs = np.array(high_pricet)
            highest = maxhigh
            defhighest_ind = np.where(allhighs == highest)[0]

            # to get all indices of definitely highest, with the indices,
            # check which highest has a greatest open, or close price.
            highopenclose = []
            for each in defhighest_ind:
                highopenclose.append(open_pricet[each])
                highopenclose.append(close_pricet[each])

            # with the max of highopenclose, we can set lowerLimit
            lowerLimit = max(highopenclose) - pricerange_bias * price_range

            # to find out all indices of elements that fit the condition --- higher than lowerLimit
            highest_ind = np.where(allhighs >= lowerLimit)[0]

            # highest_ind is a list of indices of all highs: indexofhigh2 = highest_ind[3]
            # this is ndarray type, and elements in side have already been sorted,
            # so highest_ind[0] is the earliest(first) date of index of high, where we can start from


            # now we need to do the same thing for low side
            alllows = np.array(low_pricet)
            lowest = minlow
            deflowest_ind = np.where(alllows == lowest)[0]

            lowopenclose = []
            for each in deflowest_ind:
                lowopenclose.append(open_pricet[each])
                lowopenclose.append(close_pricet[each])

            # with the min of lowopenclose, we can set higherLimit
            higherLimit = min(lowopenclose) + pricerange_bias * price_range

            # to find out all indices of elements that fit the condition --- lower than higherLimit
            lowest_ind = np.where(alllows <= higherLimit)[0]


            # let get down to business: starting from highest_ind[0],
            # to determine if the next high is bigger (later) than dayrange_bias(1/12 (or 1/13? 1/14) * day range
            # to fit this: "all these highs must be dayrange_bias (1/12 (or 1/13? 1/14) * day range apart"

            high_points = 0
            low_points = 0

            if highest_ind.size >= 3 and lowest_ind.size >= 3:

                # make sure highest/lowest are wide spread.
                # Note. removed one filter condition from below if: lowest_ind[-1] >= 2/3 * date_range
                if highest_ind[0] <= 1/3 * date_range and highest_ind[-1] >= 2/3 * date_range and lowest_ind[0] <= 1/3 * date_range:

                    min_landmarks_distance = dayrange_bias * date_range

                    # check high side: determine how many "valid" high_points in highest_ind
                    landmark = -min_landmarks_distance

                    for each in highest_ind:
                        if each - landmark >= min_landmarks_distance:
                            landmark = each
                            high_points += 1

                    # check low side: determine how many "valid" low_points in lowest_ind
                    landmark = -min_landmarks_distance

                    for each in lowest_ind:
                        if each - landmark >= min_landmarks_distance:
                            landmark = each
                            low_points += 1


                    # today high is higher than lower limit! it should be put in high alert list
                    # if it should be in high alert list
                    if high_points >= RequiredValidHighLandmarks_ha and low_points >= RequiredValidLowLandmarks_ha and todayhigh >= max(highopenclose):
                        in_list += 0b01

                    # if it should be in watch list
                    if high_points >= RequiredValidHighLandmarks_wl and low_points >= RequiredValidLowLandmarks_wl:
                        in_list += 0b10

        except Exception as e:
            print('priceTunnelChecker: ')
            print(e)
            print(open_pricet)
            in_list = 0

        return in_list


