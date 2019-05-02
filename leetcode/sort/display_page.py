class Solution(object):

    def pageDisplay(self, input_csv_array, ps):
        hosts = [line.split(',')[0] for line in input_csv_array]
        hmap = {}  # key: hostname, value: max page index of hostname entry
        pages = []
        p_start = 0

        for i, h in enumerate(hosts):
            if h not in hmap or hmap[h] < p_start:  # when hmap[h] < p_start?
                hmap[h] = p_start  # set to current page index
            print("host:{} hmap[h]:{} len(pages):{} p_start:{}".format(h, hmap[h], len(pages), p_start))
            if hmap[h] == len(pages):  # reach the last page, append one more page
                pages.append([])
            pages[hmap[h]].append(input_csv_array[i])
            hmap[h] += 1
            if len(pages[p_start]) == ps:  # content in current page is full
                p_start += 1  # start to fill in next page

        for page in pages:
            print("------page-separator-------")
            for line in page:
                print(line)


input_csv_array = [
  "1,28,300.1,SanFrancisco",
  "4,5,209.1,SanFrancisco",
  "20,7,208.1,SanFrancisco",
  "23,8,207.1,SanFrancisco",
  "16,10,206.1,Oakland",
  "1,16,205.1,SanFrancisco",
  "6,29,204.1,SanFrancisco",
  "7,20,203.1,SanFrancisco",
  "8,21,202.1,SanFrancisco",
  "2,18,201.1,SanFrancisco",
  "2,30,200.1,SanFrancisco",
  "15,27,109.1,Oakland",
  "10,13,108.1,Oakland",
  "11,26,107.1,Oakland",
  "12,9,106.1,Oakland",
  "13,1,105.1,Oakland",
  "22,17,104.1,Oakland",
  "1,2,103.1,Oakland",
  "28,24,102.1,Oakland",
  "18,14,11.1,SanJose",
  "6,25,10.1,Oakland",
  "19,15,9.1,SanJose",
  "3,19,8.1,SanJose",
  "3,11,7.1,Oakland",
  "27,12,6.1,Oakland",
  "1,3,5.1,Oakland",
  "25,4,4.1,SanJose",
  "5,6,3.1,SanJose",
  "29,22,2.1,SanJose",
  "30,23,1.1,SanJose"
]

print("*input_csv_array*")
Solution().pageDisplay(input_csv_array, ps=12)

