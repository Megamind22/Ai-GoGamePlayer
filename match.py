from agent.evaluation import return_best_point
from agent2.search import minimax_alpa_beta
from game.go import Model,WHITE,BLACK
from game.ui import UI
import pygame ,sys
import time



class Match():
    def __init__(self,agent_black=None, agent_white=None, gui=True, dir_save=None):
        self.agent_black = agent_black
        self.agent_white = agent_white
        self.model = Model()
        self.ui = UI() if gui else None
        self.dir_save = dir_save
        self.time_elapsed = None

    def start(self):
        if self.ui :
            self._start_with_ui()

    def _start_with_ui(self):
        """Start the game with GUI."""
        self.ui.initialize()

        # Take turns to play move
        while not self.model.game_over:
            if self.model.turn:
                point = self.perform_one_move(self.agent_black)
            else:
                point = self.perform_one_move(self.agent_white)
            # Apply action
            print(self.model.board)
            # Draw new point
            if self.model.ko == (point[0], point[1]):
                continue
            if self.model.place_stone(point[0], point[1]):
                self.ui.draw(point, not self.model.turn)
            # Update new legal actions and any removed groups
            if not self.model.game_over:
                myfont = pygame.font.Font('game/NotoSansDisplay-VariableFont_wdth,wght.ttf', 20)
                list = self.model.add_scores()
                lable = myfont.render("White :" + str(list[0]), True, (0, 0, 0), (255, 228, 181))
                self.ui.screen.blit(lable, (40, 10))
                lable = myfont.render("Black :" + str(list[1]), True, (0, 0, 0), (255, 228, 181))
                self.ui.screen.blit(lable, (300, 10))

            if self.model.dead_group is not None:
                #print(self.model.dead_group)
                for groubs in self.model.dead_group:
                    for point in groubs.stones:
                        self.ui.remove(point)
                    self.model.dead_group.remove(groubs)
            self.model.dead_group = None

            self.time_elapsed = time.time() - self.time_elapsed
            print(self.time_elapsed)

    def perform_one_move(self, agent):
        if agent:
            return self._move_by_agent(agent)
        else:
            return self._move_by_human()

    def _move_by_agent(self, agent):
        while not self.model.game_over:
           # list,score=minimax_alpa_beta(1,True,None,float("-inf"),float("inf"),self.model)
           # print(list)
           # print(score)
           # x = list[0]
           # y = list[1]
            #if not self.model.check_if_neigh(x, y):
             #   list, score = minimax_alpa_beta(1, True, None, float("-inf"), float("inf"), self.model)
              #  x = list[0]
               # y = list[1]
            #point=(x,y)
             self.time_elapsed = time.time()
             point=return_best_point()
             return point

    def passing(self , event):
        myfont = pygame.font.Font('game/NotoSansDisplay-VariableFont_wdth,wght.ttf', 20)
        if (event.pos[0] >= 500 and event.pos[0] <= 550) and (event.pos[1] >= 10 and event.pos[1] <= 30):
            self.model.has_passed = True
            list = self.model.add_scores()
            if list[0] > list[1]:
                lable = myfont.render(" White wins! ", True, (0, 0, 0), (255, 255, 0))
                self.ui.screen.blit(lable, (600, 10))
                pygame.display.update()
                pygame.time.wait(5000)
                sys.exit(0)
            elif list[0] == list[1]:
                lable = myfont.render(" equality  ", True, (0, 0, 0), (255, 255, 0))
                self.ui.screen.blit(lable, (600, 10))
                pygame.display.update()
                pygame.time.wait(5000)
                sys.exit(0)
            else:
                lable = myfont.render(" BLACK wins! ", True, (0, 0, 0), (255, 255, 0))
                self.ui.screen.blit(lable, (600, 10))
                pygame.display.update()
                pygame.time.wait(5000)
                sys.exit(0)

    def _move_by_human(self):
        while True:
            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    myfont = pygame.font.Font('game/NotoSansDisplay-VariableFont_wdth,wght.ttf', 20)
                    lable = myfont.render("PASS :", True, (0, 0, 0), (255, 228, 181))
                    self.ui.screen.blit(lable, (500, 10))
                    self.passing(event)

                    if event.button == 1 and self.ui.outline.collidepoint(event.pos):
                        x = int(round(((event.pos[0] - 45) / 40.0), 0))
                        y = int(round(((event.pos[1] - 45) / 40.0), 0))
                        print(x, y)
                        point = (x, y)


                        if self.model.check_if_neigh(x, y):
                            return point


def main():
    play = input("Enter Number of Player...!")
    if int(play)==2:
        match = Match(agent_black=False, agent_white=False, gui=True, dir_save=None)
    else:
        match = Match(agent_black=True, agent_white=False, gui=True, dir_save=None)

    match.start()
    print('Match starts!')


if __name__ == '__main__':
     #match = Match()
    # match = Match(agent_black=RandomAgent('BLACK'))
    # match = Match(agent_black=RandomAgent('BLACK'), agent_white=RandomAgent('WHITE'), gui=True)
    # match = Match(agent_black=RandomAgent('BLACK'), agent_white=RandomAgent('WHITE'), gui=False)
    # match.start()
    # print(match.winner + ' wins!')
    # print('Match ends in ' + str(match.time_elapsed) + ' seconds')
    # print('Match ends in ' + str(match.counter_move) + ' moves')
    main()