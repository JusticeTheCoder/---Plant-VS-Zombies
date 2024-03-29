__author__ = 'Allen W'

import os
import json
import pygame as pg
from .. import tool
from .. import constants as c
from ..component import map, plant, zombie, menubar

class Level(tool.State):
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.map_y_len = c.GRID_Y_LEN
        self.map = map.Map(c.GRID_X_LEN, self.map_y_len)
        
        self.loadMap()
        
        self.menubar = menubar.MenuBar(menubar.card_list, self.map_data[c.INIT_SUN_NAME])
        self.drag_plant = False
        self.hint_image = None
        self.hint_plant = False
        
        self.produce_sun = True
        self.sun_timer = current_time
        
        self.removeMouseImage()
        self.setupBackground()
        self.setupGroups()
        self.setupZombies()
    
    def loadMap(self):
        map_file = 'level_' + str(self.game_info[c.LEVEL_NUM]) + '.json'
        file_path = os.path.join('source', 'data', 'map', map_file)
        f = open(file_path)
        self.map_data = json.load(f)
        f.close()
    
    def setupBackground(self):
        img_index = self.map_data[c.BACKGROUND_TYPE]
        self.background = tool.GFX[c.BACKGROUND_NAME][img_index]
        self.bg_rect = self.background.get_rect()

        self.level = pg.Surface((self.bg_rect.w, self.bg_rect.h)).convert()
        self.viewport = tool.SCREEN.get_rect(bottom=self.bg_rect.bottom)
        self.viewport.x += 230
    
    def setupGroups(self):
        self.sun_group = pg.sprite.Group()
        self.head_group = pg.sprite.Group()

        self.plant_groups = []
        self.zombie_groups = []
        self.bullet_groups = []
        for i in range(self.map_y_len):
            self.plant_groups.append(pg.sprite.Group())
            self.zombie_groups.append(pg.sprite.Group())
            self.bullet_groups.append(pg.sprite.Group())
    
    def setupZombies(self):
        def takeTime(element):
            return element[0]

        self.zombie_list = []
        for data in self.map_data[c.ZOMBIE_LIST]:
            self.zombie_list.append((data['time'], data['name'], data['map_y']))
        self.zombie_start_time = 0
        self.zombie_list.sort(key=takeTime)

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if self.zombie_start_time == 0:
            self.zombie_start_time = self.current_time
        elif len(self.zombie_list) > 0:
            data = self.zombie_list[0]
            if  data[0] <= (self.current_time - self.zombie_start_time):
                self.createZombie(data[1], data[2])
                self.zombie_list.remove(data)

        for i in range(self.map_y_len):
            self.bullet_groups[i].update(self.game_info)
            self.plant_groups[i].update(self.game_info)
            self.zombie_groups[i].update(self.game_info)
        self.head_group.update(self.game_info)
        self.sun_group.update(self.game_info)
        
        if not self.drag_plant and mouse_pos and mouse_click[0]:
            result = self.menubar.checkCardClick(mouse_pos)
            if result:
                self.setupMouseImage(result[0], result[1])
        elif self.drag_plant:
            if mouse_click[1]:
                self.removeMouseImage()
            elif mouse_click[0]:
                if self.menubar.checkMenuBarClick(mouse_pos):
                    self.removeMouseImage()
                else:
                    self.addPlant()
            elif mouse_pos is None:
                self.setupHintImage()
        
        if self.produce_sun:
            if(self.current_time - self.sun_timer) > c.PRODUCE_SUN_INTERVAL:
                self.sun_timer = self.current_time
                map_x, map_y = self.map.getRandomMapIndex()
                x, y = self.map.getMapGridPos(map_x, map_y)
                self.sun_group.add(plant.Sun(x, 0, x, y))
            if not self.drag_plant and mouse_pos and mouse_click[0]:
                for sun in self.sun_group:
                    if sun.checkCollision(mouse_pos[0], mouse_pos[1]):
                        self.menubar.increaseSunValue(c.SUN_VALUE)

        self.checkBulletCollisions()
        self.checkZombieCollisions()
        self.checkPlants()
        self.checkGameState()
        self.draw(surface)
    
    def createZombie(self, name, map_y):
        x, y = self.map.getMapGridPos(0, map_y)
        if name == c.NORMAL_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.NormalZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.CONEHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.ConeHeadZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.BUCKETHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.BucketHeadZombie(c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.FLAG_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.FlagZombie(c.ZOMBIE_START_X, y, self.head_group))

    def canSeedPlant(self): #判断当前坐标能否种植物
        x, y = pg.mouse.get_pos()
        return self.map.showPlant(x, y)
        
    def addPlant(self):
        pos = self.canSeedPlant()
        if pos is None:
            return

        if self.hint_image is None:
            self.setupHintImage()
        x, y = self.hint_rect.centerx, self.hint_rect.bottom
        map_x, map_y = self.map.getMapIndex(x, y)
        if self.plant_name == c.SUNFLOWER:
            self.plant_groups[map_y].add(plant.SunFlower(x, y, self.sun_group))
        elif self.plant_name == c.PEASHOOTER:
            self.plant_groups[map_y].add(plant.PeaShooter(x, y, self.bullet_groups[map_y]))
        elif self.plant_name == c.SNOWPEASHOOTER:
            self.plant_groups[map_y].add(plant.SnowPeaShooter(x, y, self.bullet_groups[map_y]))
        elif self.plant_name == c.WALLNUT:
            self.plant_groups[map_y].add(plant.WallNut(x, y))
        elif self.plant_name == c.CHERRYBOMB:
            self.plant_groups[map_y].add(plant.CherryBomb(x, y))

        self.menubar.decreaseSunValue(self.plant_cost)
        self.map.setMapGridType(map_x, map_y, c.MAP_EXIST)
        self.removeMouseImage()
        

    def setupHintImage(self):#setupHintImage 函数：如果当前鼠标位置能种植物，且有选择了一个植物卡片，则设置self.hint_image 显示当前会在哪一个方格中种植物，self.hint_rect 是植物种的坐标位置。
        pos = self.canSeedPlant()
        if pos and self.mouse_image:
            if (self.hint_image and pos[0] == self.hint_rect.x and
                pos[1] == self.hint_rect.y):
                return
            width, height = self.mouse_rect.w, self.mouse_rect.h
            image = pg.Surface([width, height])
            image.blit(self.mouse_image, (0, 0), (0, 0, width, height))
            image.set_colorkey(c.BLACK)
            image.set_alpha(128)
            self.hint_image = image
            self.hint_rect = image.get_rect()
            self.hint_rect.centerx = pos[0]
            self.hint_rect.bottom = pos[1]
            self.hint_plant = True
        else:
            self.hint_plant = False


#setupMouseImage 函数实现鼠标图片切换为选中的植物
# self.mouse_image ：根据 plant_name 获取选中的植物图片
# self.mouse_rect：选中植物图片的位置，在drawMouseShow函数中，需要将植物图片的位置设置成当前鼠标的位置
# pg.mouse.set_visible(False)：隐藏默认的鼠标显示，这样效果就是鼠标图片切换为选中的植物了。

    def setupMouseImage(self, plant_name, plant_cost):
        frame_list = tool.GFX[plant_name]
        rect = frame_list[0].get_rect()
        width, height = rect.w, rect.h

        self.mouse_image = tool.get_image(frame_list[0], 0, 0, width, height, c.BLACK, 1)
        self.mouse_rect = self.mouse_image.get_rect()
        pg.mouse.set_visible(False)
        self.drag_plant = True
        self.plant_name = plant_name
        self.plant_cost = plant_cost








    def removeMouseImage(self):
        pg.mouse.set_visible(True)
        self.drag_plant = False
        self.mouse_image = None
        self.hint_image = None
        self.hint_plant = False









    def checkBulletCollisions(self):
        collided_func = pg.sprite.collide_circle_ratio(0.7)
        for i in range(self.map_y_len):
            for bullet in self.bullet_groups[i]:
                if bullet.state == c.FLY:
                    zombie = pg.sprite.spritecollideany(bullet, self.zombie_groups[i], collided_func)
                    if zombie and zombie.state != c.DIE:
                        zombie.setDamage(bullet.damage)
                        bullet.setExplode()
    









    def checkZombieCollisions(self):
        collided_func = pg.sprite.collide_circle_ratio(0.7)
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                plant = pg.sprite.spritecollideany(zombie, self.plant_groups[i], collided_func)
                if plant and zombie.state == c.WALK:
                    zombie.setAttack(plant)
                    plant.setAttacked()
    








    def boomZombies(self, x, map_y):
        for i in range(self.map_y_len):
            if abs(i - map_y) > 1:
                continue
            for zombie in self.zombie_groups[i]:
                if abs(zombie.rect.x - x) <= c.GRID_X_SIZE:
                    zombie.setBoomDie()











    def killPlant(self, plant):
        map_x, map_y = self.map.getMapIndex(plant.rect.centerx, plant.rect.bottom)
        self.map.setMapGridType(map_x, map_y, c.MAP_EMPTY)
        if plant.name == c.CHERRYBOMB:
            self.boomZombies(plant.rect.centerx, map_y)
        plant.kill()












    def checkPlants(self):
        for i in range(self.map_y_len):
            if len(self.zombie_groups[i]) > 0:
                for plant in self.plant_groups[i]:
                    if plant.state == c.IDLE:
                        plant.setAttack()
                    if plant.health <= 0:
                        self.killPlant(plant)
            else:
                for plant in self.plant_groups[i]:
                    if plant.state == c.ATTACK:
                        plant.setIdle()
                    if plant.health <= 0:
                        self.killPlant(plant)
    








    def checkVictory(self):
        if len(self.zombie_list) > 0:
            return False
        for i in range(self.map_y_len):
            if len(self.zombie_groups[i]) > 0:
                return False
        return True
    
    def checkLose(self):
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                if zombie.rect.right < 0:
                    return True
        return False

    def checkGameState(self):
        if self.checkVictory():
            self.game_info[c.LEVEL_NUM] += 1
            self.next = c.GAME_VICTORY
            self.done = True
        elif self.checkLose():
            self.next = c.GAME_LOSE
            self.done = True

    def drawMouseShow(self, surface):
        if self.hint_plant:
            surface.blit(self.hint_image, self.hint_rect)
        x, y = pg.mouse.get_pos()
        self.mouse_rect.centerx = x
        self.mouse_rect.centery = y
        surface.blit(self.mouse_image, self.mouse_rect)
            
    def draw(self, surface):
        self.level.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.level, (0,0), self.viewport)
        self.menubar.draw(surface)
        for i in range(self.map_y_len):
            self.plant_groups[i].draw(surface)
            self.zombie_groups[i].draw(surface)
            self.bullet_groups[i].draw(surface)
        self.head_group.draw(surface)
        self.sun_group.draw(surface)

        if self.drag_plant:
            self.drawMouseShow(surface)