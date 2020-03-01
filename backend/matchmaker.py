import time
class Matchmaker:
    '''
    Class to match make a gameroom based on a request
    '''

    @staticmethod
    def matchmake(request, fitness=0.75, offset=0.1):
        # Pseudocode
        # start = time.time()
        # while request.is_alive(): 
        #     for room in rooms(request, offset):
        #         if match_quality(request, room) < fitness:
        #             if time.time - start > 30:
        #                 offset <- offset + offset * 0.5
        #                 fitness <- fitness * 0.75
        #             continue
        #         else:
        #             match(request, room)
        #             break
        pass
