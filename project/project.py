import pygame
from random import randint, choice


class Main:
    def __init__(self):
        pygame.init()
        size = width, height = 800, 712
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Flappy Bird')
        self.font1 = pygame.font.Font(None, 35)
        self.font2 = pygame.font.Font('data/font.otf', 80)
        self.font3 = pygame.font.Font('data/font.otf', 50)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.button1 = pygame.Rect(225, 156, 350, 100)
        self.button2 = pygame.Rect(225, 306, 350, 100)
        self.button3 = pygame.Rect(225, 456, 350, 100)
        self.button4 = pygame.Rect(680, 10, 100, 60)
        self.text1 = pygame.Rect(190, 206, 420, 100)
        self.text2 = pygame.Rect(190, 406, 420, 100)
        self.point_sound = pygame.mixer.Sound('data/point.mp3')
        self.hit_sound = pygame.mixer.Sound('data/hit.wav')
        self.potion_sound = pygame.mixer.Sound('data/potionsound.mp3')
        self.game_over_sound = pygame.mixer.Sound('data/die.wav')
        self.swoosh_sound = pygame.mixer.Sound('data/swoosh.wav')
        self.wing_sound = pygame.mixer.Sound('data/wing.wav')
        self.sound_counter = 0
        self.flag_die = True
        self.y, self.speed, self.a = height // 2, 0, 0
        self.bird = pygame.Rect(width // 3, self.y, 34, 24)
        self.state = 'start'
        self.time_start = 0
        self.time_pause = 0
        self.time_scores = 0
        self.counter_speed = 0
        self.timer_sound = 0
        self.running = True
        self.results = False
        self.timer_potion = 0
        self.pipes = []
        self.bases = []
        self.potions = []
        self.p_p = 0
        self.f = True
        self.distance = [200, 250, 300, 350, 400, 450, 500, 550]
        self.bases.append(pygame.Rect(0, height - 113, 338, 113))
        self.background = []
        self.sound = pygame.Rect(600, 655, 52, 52)
        self.background.append(pygame.Rect(0, 0, 338, 600))
        self.imgsound_on = pygame.image.load('data/sound_on.png')
        self.imgsound_off = pygame.image.load('data/sound_off.png')
        self.day = ['day', 'night']
        self.pipe_color = ['red', 'green']
        tmp = choice(self.day)
        self.imgBG = pygame.image.load(f'data/background-{tmp}.png')
        self.imgbird = pygame.image.load('data/redbirds.png')
        tmp = choice(self.pipe_color)
        self.imgpd = pygame.image.load(f'data/pipe-{tmp}-up.png')
        self.imgpup = pygame.image.load(f'data/pipe-{tmp}-down.png')
        self.imgbase = pygame.image.load('data/base.png')
        self.imgpotion = pygame.image.load('data/greenpotion2.png')
        self.imgbutton = pygame.image.load('data/restart.png')
        self.imggameover = pygame.image.load('data/gameover.png')
        self.imgback = pygame.image.load('data/back.png')
        self.imgpause = pygame.image.load('data/pause.png')
        self.imgplay = pygame.image.load('data/play.png')
        self.game_over_text = pygame.Rect(width // 2 - 120, height // 3, 192, 42)
        self.button_restart = pygame.Rect(10, height - 50, 120, 42)
        self.button_back = pygame.Rect(660, 10, 117, 42)
        self.button_pause = pygame.Rect(660, 660, 117, 42)
        self.button_play = pygame.Rect(660, 660, 117, 42)
        self.paused = False
        self.menu_show = True
        self.sound_control = True
        self.counter = 0
        self.n = 0
        self.lives = 3
        self.scores = 0
        self.tot2 = False
        self.tot3 = False
        self.tot4 = False

    def show_menu(self):
        menu_background = pygame.image.load('data/menu.jpeg')

        while self.menu_show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
            self.screen.blit(menu_background, (0, 0))
            self.draw_bmenu(225, 156, self.button1, 'Start game', 20, self.font2)
            self.draw_bmenu(225, 306, self.button2, 'Results', 75, self.font2)
            self.draw_bmenu(225, 456, self.button3, 'Quit', 110, self.font2)

            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.button1.collidepoint(pos):
                    self.menu_show = False
                    self.running = True
                    self.restart()
                    self.update()

                elif self.button2.collidepoint(pos):
                    self.menu_show = False
                    self.results = True
                    self.show_results()

                elif self.button3.collidepoint(pos):
                    pygame.quit()
                    quit()

            pygame.display.update()
            self.clock.tick(self.fps)

    def draw_bmenu(self, x, y, rect, name, gap, font):
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos):
            pygame.draw.rect(self.screen, pygame.Color("#5FB425"), rect)
        else:
            pygame.draw.rect(self.screen, pygame.Color("#5FDE25"), rect)
        text = font.render(name, True, pygame.Color('black'))
        self.screen.blit(text, (x + gap, y + 10))

    def show_results(self):
        res_background = pygame.image.load('data/menu.jpeg')
        tmp = []
        f = open('data/results.txt')
        for string in f.readlines():
            tmp.append(int(string[:-1]))
        f.close()
        if len(tmp):
            max_score = max(tmp)
            last_score = tmp[-1]
        else:
            max_score = ''
            last_score = ''

        while self.results:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()

            self.screen.blit(res_background, (0, 0))

            self.draw_results(190, 206, self.text1, f'Record: {max_score}', 10)
            self.draw_results(190, 406, self.text2, f'Last score: {last_score}', 10)
            self.draw_bmenu(680, 10, self.button4, 'Back', 10, self.font3)

            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.button4.collidepoint(pos):
                    self.results = False
                    self.menu_show = True

            pygame.display.update()
            self.clock.tick(self.fps)

    def draw_results(self, x, y, rect, name, gap):
        pygame.draw.rect(self.screen, pygame.Color("#5FDE25"), rect)
        text = self.font2.render(name, True, pygame.Color('black'))
        self.screen.blit(text, (x + gap, y + 10))

    def update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()

            mouse = [0]
            pos = pygame.mouse.get_pos()
            if not self.button_pause.collidepoint(pos) and not self.button_back.collidepoint(pos) and \
                    not self.sound.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    mouse = pygame.mouse.get_pressed()

            keys = pygame.key.get_pressed()
            self.click = mouse[0] or keys[pygame.K_SPACE] or keys[pygame.K_UP]

            if self.time_start > 0:
                self.time_start -= 1

            if self.time_pause > 0:
                self.time_pause -= 1

            if self.timer_potion > 0:
                self.timer_potion -= 1

            if self.timer_sound > 0:
                self.timer_sound -= 1

            if not self.timer_potion:
                if self.tot2:
                    self.tot2 = False
                if self.tot3:
                    self.tot3 = False
                if self.tot4:
                    self.tot4 = False

            if self.counter > 0 and not self.tot2 and not self.tot3 and not self.tot4:
                tmp = randint(5, 8)
                if self.scores >= tmp * self.counter:
                    self.f = True

            self.n = (self.n + 0.2) % 4

            self.background_move()
            self.pipe_move()
            self.base_move()

            if self.state == 'start':
                self.start()
            elif self.state == 'play':
                self.play()
            elif self.state == 'fall':
                self.fall()
            elif self.state == 'gameover':
                self.game_over()

            self.screen.fill((0, 0, 0))

            for bg in self.background:
                self.screen.blit(self.imgBG, bg)

            for pipe in self.pipes:
                if pipe.y == 0:
                    rect = self.imgpup.get_rect(bottomleft=pipe.bottomleft)
                    self.screen.blit(self.imgpup, rect)
                else:
                    rect = self.imgpd.get_rect(topleft=pipe.topleft)
                    self.screen.blit(self.imgpd, rect)

            if len(self.potions):
                rect = self.imgpotion.get_rect(bottomleft=self.potions[0].bottomleft)
                self.screen.blit(self.imgpotion, rect)

            for b in self.bases:
                self.screen.blit(self.imgbase, b)

            if self.state == 'gameover':
                image = self.imgbird.subsurface(34, 0, 34, 24)
                image = pygame.transform.rotate(image, -90)
                self.draw_button()
            else:
                if not self.sound_counter and self.sound_control:
                    self.wing_sound.play()
                image = self.imgbird.subsurface(34 * int(self.n), 0, 34, 24)
                image = pygame.transform.rotate(image, -self.speed * 2)

            self.screen.blit(image, self.bird)
            if not self.tot2 and not self.tot4:
                self.sound_counter = (self.sound_counter + 1) % 30
            else:
                self.sound_counter = (self.sound_counter + 1) % 15
            self.screen.blit(self.imgpause, self.button_pause)

            self.screen.blit(self.imgback, self.button_back)

            if self.sound_control:
                self.screen.blit(self.imgsound_off, self.sound)
            else:
                self.screen.blit(self.imgsound_on, self.sound)

            text = self.font1.render('Scores: ' + str(self.scores), True, pygame.Color('black'))
            self.screen.blit(text, (10, 10))

            text = self.font1.render('Lives: ' + str(self.lives), True, pygame.Color('black'))
            self.screen.blit(text, (10, 45))

            pygame.display.update()
            self.clock.tick(self.fps)

    def back_check(self):
        pos = pygame.mouse.get_pos()
        if self.button_back.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.pipes.clear()
            self.potions.clear()
            self.menu_show = True
            self.running = False

    def mute_check(self):
        pos = pygame.mouse.get_pos()
        if self.sound.collidepoint(pos) and pygame.mouse.get_pressed()[0] and not self.timer_sound:
            if self.sound_control:
                self.sound_control = False
                self.timer_sound = 60
            else:
                self.sound_control = True
                self.timer_sound = 60

    def pause_make(self):
        self.paused = True
        while self.paused and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
            self.back_check()
            if self.time_pause > 0:
                self.time_pause -= 1
            pos = pygame.mouse.get_pos()
            if ((self.button_play.collidepoint(pos) and pygame.mouse.get_pressed()[0])
                or pygame.key.get_pressed()[pygame.K_p]) and self.time_pause == 0:
                self.paused = False
                self.time_pause = 30

            self.screen.blit(self.imgplay, self.button_play)
            pygame.display.update()
            self.clock.tick(self.fps)

    def pipe_move(self):
        if self.state != 'gameover':
            for i in range(len(self.pipes) - 1, -1, -1):
                pipe = self.pipes[i]
                if self.tot2:
                    pipe.x -= 5
                elif self.tot4:
                    pipe.x -= 8
                else:
                    pipe.x -= 3

                if pipe.right < 0:
                    self.pipes.remove(pipe)

            if len(self.potions):
                self.potions[0].x -= 3
                if self.potions[0].right < 0:
                    self.potions.clear()

    def draw_button(self):
        self.screen.blit(self.imggameover, self.game_over_text)
        self.screen.blit(self.imgbutton, self.button_restart)

        pos = pygame.mouse.get_pos()

        if self.button_restart.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.restart()

    def background_move(self):
        if self.state != 'gameover':
            for i in range(len(self.background) - 1, -1, -1):
                bg = self.background[i]
                if self.tot2:
                    bg.x -= 2
                else:
                    bg.x -= 1

                if bg.right < 0:
                    self.background.remove(bg)

                if self.background[-1].right <= self.width:
                    self.background.append(pygame.Rect(self.background[-1].right, 0, 338, 600))

    def base_move(self):
        if self.state != 'gameover':
            for i in range(len(self.bases) - 1, -1, -1):
                b = self.bases[i]
                if self.tot2:
                    b.x -= 5
                elif self.tot4:
                    b.x -= 8
                else:
                    b.x -= 3

                if b.right < 0:
                    self.bases.remove(b)

                if self.bases[-1].right <= self.width:
                    self.bases.append(pygame.Rect(self.bases[-1].right, self.height - 113, 338, 113))

    def start(self):
        self.back_check()
        self.mute_check()
        if self.click and self.time_start == 0 and len(self.pipes) == 0:
            self.state = 'play'
        self.y += (self.height // 2 - self.y) * 0.1
        self.bird.y = self.y

    def play(self):
        self.back_check()
        self.mute_check()
        if self.click:
            if not self.tot3:
                self.a = -2
            else:
                self.a = 2
        else:
            self.a = 0

        self.y += self.speed

        pos = pygame.mouse.get_pos()
        if ((self.button_pause.collidepoint(pos) and pygame.mouse.get_pressed()[0])
            or pygame.key.get_pressed()[pygame.K_p]) and self.time_pause == 0:
            self.time_pause = 30
            self.pause_make()

        if self.tot3:
            self.speed = (self.speed + self.a - 1) * 0.95
        else:
            self.speed = (self.speed + self.a + 1) * 0.95
        self.bird.y = self.y

        self.check()

        when = choice(self.distance)
        if len(self.pipes) == 0 or self.pipes[len(self.pipes) - 1].x < self.width - when:
            gap = randint(-100, 100)
            self.pipes.append(pygame.Rect(self.width, 0, 52, 200 + gap))
            self.pipes.append(pygame.Rect(self.width, 400 + gap, 52, 320))
            if self.scores >= 5 and self.f:
                self.f = False
                self.make_potion()
                self.counter += 1
        if self.tot2:
            if self.counter_speed > 1:
                self.time_scores = (self.time_scores + 1) % 2
            else:
                self.time_scores = (self.time_scores + 1) % 4
            self.counter_speed = (self.counter_speed + 1) % 4
        elif self.tot4:
            self.time_scores = (self.time_scores + 1) % 2
        else:
            self.time_scores = (self.time_scores + 1) % 5

    def make_potion(self):
        border_up = self.pipes[-2].height
        border_down = self.pipes[-1].y
        y = ((border_down - border_up) - 44) // 2
        self.potions.append(pygame.Rect(self.width, border_up + y, 30, 44))

    def check(self):
        if self.bird.top < 0 or self.bird.bottom > self.height - 113:
            self.state = 'fall'
            if self.sound_control:
                self.hit_sound.play()

        for pipe in self.pipes:
            if self.bird.colliderect(pipe):
                self.state = 'fall'
                if self.sound_control:
                    self.hit_sound.play()
            if pipe.left < self.bird.left and pipe.right > self.bird.right and pipe.y == 0 and not self.time_scores:
                self.scores += 1
                if self.sound_control:
                    self.point_sound.play()

        if len(self.potions):
            if self.bird.colliderect(self.potions[0]):
                if self.sound_control:
                    self.potion_sound.play()
                self.potions.clear()
                self.trick_or_treat()

    def trick_or_treat(self):
        if self.lives > 1:
            choose = randint(1, 5)
        else:
            choose = randint(1, 4)
        if choose == 1:
            self.lives += 1
        elif choose == 2:
            self.timer_potion = 600
            self.tot2 = True
        elif choose == 4:
            self.tot4 = True
            self.timer_potion = 600
        elif choose == 3:
            self.timer_potion = 600
            self.tot3 = True
            self.pipes.clear()
        elif choose == 5:
            self.lives -= 1

    def fall(self):
        self.back_check()
        self.mute_check()
        self.speed, self.a = 0, 0
        self.timer_potion = 0
        self.tot2 = False
        self.tot3 = False
        self.tot4 = False
        if self.lives > 1:
            self.state = 'start'
            self.time_start = 60
            self.lives -= 1
        else:
            self.lives -= 1
            self.game_over()

    def game_over(self):
        self.back_check()
        self.mute_check()
        if self.flag_die:
            self.flag_die = False
            if self.sound_control:
                self.game_over_sound.play()
            self.score_count()
        self.state = 'gameover'
        self.y += (self.height - 133 - self.y) * 0.1
        self.bird.y = self.y

    def score_count(self):
        f = open('data/results.txt', 'a')
        f.write(str(self.scores) + '\n')
        f.close()

    def restart(self):
        self.scores = 0
        self.lives = 3
        self.counter = 0
        self.f = True
        self.flag_die = True
        self.pipes.clear()
        self.potions.clear()
        self.bird.y = self.height // 2
        self.state = 'start'
        self.time_start = 60
        tmp = choice(self.day)
        self.imgBG = pygame.image.load(f'data/background-{tmp}.png')
        tmp = choice(self.pipe_color)
        self.imgpd = pygame.image.load(f'data/pipe-{tmp}-up.png')
        self.imgpup = pygame.image.load(f'data/pipe-{tmp}-down.png')


g = Main()
g.show_menu()
