import pygame
from utils.helper_function import get_uid

class UnitAnimation:
    def __init__(self, surface, x, y, name, is_ai = False):
        self.__surface = surface
        # get the unit's name
        self.name = name
        self.uid = get_uid(name)
        # the start index of frame
        self.frame_idx = 0
        # unit's current status
        self.status = 0 # 0: idle 1: atk 2: sp_atk 3: hurt 4: dead
        self.update_time = pygame.time.get_ticks()
        # check if the unit is AI
        self.is_ai = is_ai
        # initialize two animation lists to store images
        self.animation_list_l = []
        self.animation_list_r = []
        # set up two animation images lists
        self.set_up()
        self.animation_list = self.animation_list_r if is_ai else self.animation_list_l
        # current animation image
        self.img = self.animation_list_r[self.status][self.frame_idx]
        # image's rect
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        # duration time of animation
        self.status_duration = 2000
        # start time of animation of new status
        self.status_start_time = 0

    def set_up(self):
        # list of the length of idle images
        idle_list = [4, 6, 5, 3, 5, 5]
        idle_len = idle_list[self.uid - 1]

        # list of the length of atk images
        atk_list = [4, 5, 5, 9, 6, 4]
        atk_len = atk_list[self.uid - 1]

        # list of the length of sp_atk images
        sp_list = [14, 5, 6, 4, 10, 7]
        sp_len = sp_list[self.uid - 1]

        # list of the length of hurt images
        hurt_list = [3, 3, 2, 3, 2, 4]
        hurt_len = hurt_list[self.uid - 1]

        # list of the length of hurt images
        dead_list = [3, 4, 4, 3, 5, 4]
        dead_len = dead_list[self.uid - 1]

        # load idle images
        temp_list = []
        for i in range(idle_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/idle/{i}l.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_l.append(temp_list)
        # load atk images
        temp_list = []
        for i in range(atk_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/atk/{i}l.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_l.append(temp_list)
        # load sp_atk images
        temp_list = []
        for i in range(sp_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/sp_atk/{i}l.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_l.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(hurt_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/hurt/{i}l.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_l.append(temp_list)
        # load dead images
        temp_list = []
        for i in range(dead_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/dead/{i}l.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_l.append(temp_list)

        # load idle images
        temp_list = []
        for i in range(idle_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/idle/{i}r.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_r.append(temp_list)
        # load atk images
        temp_list = []
        for i in range(atk_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/atk/{i}r.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_r.append(temp_list)
        # load sp_atk images
        temp_list = []
        for i in range(sp_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/sp_atk/{i}r.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_r.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(hurt_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/hurt/{i}r.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_r.append(temp_list)
        # load dead images
        temp_list = []
        for i in range(dead_len):
            img = pygame.image.load(f'resources/images/units/{self.name}/dead/{i}r.png')
            img = pygame.transform.scale(img, (128, 76)).convert_alpha()
            temp_list.append(img)
        self.animation_list_r.append(temp_list)

    # getters
    def get_rect(self):
        return self.rect

    def set_status(self, status):
        # set unit's status
        self.status = status
        # get the start time of the new status
        self.status_start_time = pygame.time.get_ticks()

    def update(self):
        # get current time
        current_time = pygame.time.get_ticks()

        # if the new animation is end, change status to idle status (0)
        if current_time - self.status_start_time >= self.status_duration and self.status != 4:
            self.set_status(0)
            return

        # control the time of changing frames
        animation_cooldown = 300

        # reset the frame to 0
        if self.frame_idx >= len(self.animation_list[self.status]):
            # if the unit status is dead(4), stay at the last frame of the dead animation
            if self.status == 4:
                self.frame_idx = len(self.animation_list[self.status]) - 1
            else:
                # otherwise, reset the frame index to 0
                self.frame_idx = 0

        # get unit's current image
        self.img = self.animation_list[self.status][self.frame_idx]
        # change the frame of the image
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            # increment the frame by 1
            self.frame_idx += 1
            # update the update time
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        # draw the current image on the display surface
        self.__surface.blit(self.img, self.rect)