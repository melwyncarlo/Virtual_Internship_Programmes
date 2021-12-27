# Vax-Man, a re-implementation of Pacman, in Python, with PyGame.
# Forked from: https://github.com/hbokmann/Pacman

# Edited by Melwyn Francis Carlo (2021)

# Video link: https://youtu.be/ZrqZEC6DvMc

import time
import pygame

# Ghosts multiply themselves every thirty seconds.
GHOST_MULTIPLICATION_TIME_GAP = 30

# Thirty-two times for each ghost type.
MAXIMUM_GHOSTS = 32 * 4;

indigo    = (  85,  48, 141 )
yellow    = ( 255, 255,   0 )
darkRed   = ( 201,  33,  30 )
darkGrey  = (  28,  28,  28 )
lightGrey = ( 238, 238, 238 )

Vaxman_icon=pygame.image.load('images/Vaxman_Big.png')
pygame.display.set_icon(Vaxman_icon)

# Add music
# Spook4 by PeriTune | http://peritune.com
# Attribution 4.0 International (CC BY 4.0)
# https://creativecommons.org/licenses/by/4.0/
# Music promoted by https://www.chosic.com/free-music/all/
pygame.mixer.init()
pygame.mixer.music.load('peritune-spook4.mp3')
pygame.mixer.music.play(-1, 0.0)

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make an indigo wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # Loop through the list. Create the wall, add it to the list.
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], indigo)
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    # Return our new list.
    return wall_list

def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282, 242, 42, 2, lightGrey))
      all_sprites_list.add(gate)
      return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(lightGrey)
        self.image.set_colorkey(lightGrey)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
  
    # Set speed vector
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self, x, y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert_alpha()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls,gate):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y

#Inheritime Player klassist
class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif ghost == "clyde":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]

Pinky_directions = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Blinky_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Inky_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Clyde_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pl = len(Pinky_directions)  - 1
bl = len(Blinky_directions) - 1
il = len(Inky_directions)   - 1
cl = len(Clyde_directions)  - 1

# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Melly the Vax-Man')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a dark grey background
background.fill(darkGrey)



clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

#default locations for Vax-Man and ghosts
w   =  303 - 16         # Width
p_h =   19 + (7 * 60)   # Vax-Man height
m_h =   19 + (4 * 60)   # Monster height
b_h =   19 + (3 * 60)   # Binky height
i_w =  303 -  16 - 32   # Inky width
c_w =  303 + (32 - 16)  # Clyde width

def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  ghosts_list = pygame.sprite.RenderPlain()

  vaxman_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)

  # Create the player paddle object
  Vaxman = Player(w, p_h, "images/Vaxman_Small.png")
  all_sprites_list.add(Vaxman)
  vaxman_collide.add(Vaxman)

  Blinkies = []
  Pinkies  = []
  Inkies   = []
  Clydes   = []

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, vaxman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0

  done = False

  i = 0

  previousTime = 0;

  while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

      currentTime = time.time();
      deltaTime   = currentTime - previousTime;

      if previousTime == 0 or deltaTime > GHOST_MULTIPLICATION_TIME_GAP:

            if previousTime == 0 or Blinkies:
                Blinkies.append( { "entity" : Ghost(w,   b_h, "images/Blinky.png"), "turn" : 0, "steps" : 0 } )
                ghosts_list.add(Blinkies[-1]["entity"])
                all_sprites_list.add(Blinkies[-1]["entity"])

            if previousTime == 0 or Pinkies:
                Pinkies.append(  { "entity" : Ghost(w,   m_h, "images/Pinky.png"),  "turn" : 0, "steps" : 0 } )
                ghosts_list.add(Pinkies[-1]["entity"])
                all_sprites_list.add(Pinkies[-1]["entity"])

            if previousTime == 0 or Inkies:
                Inkies.append(   { "entity" : Ghost(i_w, m_h, "images/Inky.png"),   "turn" : 0, "steps" : 0 } )
                ghosts_list.add(Inkies[-1]["entity"])
                all_sprites_list.add(Inkies[-1]["entity"])

            if previousTime == 0 or Clydes:
                Clydes.append(   { "entity" : Ghost(c_w, m_h, "images/Clyde.png"),  "turn" : 0, "steps" : 0 } )
                ghosts_list.add(Clydes[-1]["entity"])
                all_sprites_list.add(Clydes[-1]["entity"])

            previousTime = currentTime

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Vaxman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Vaxman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Vaxman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Vaxman.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Vaxman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Vaxman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Vaxman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Vaxman.changespeed(0,-30)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Vaxman.update(wall_list, gate)

      for Pinky in Pinkies:
          returned = Pinky["entity"].changespeed(Pinky_directions, False, Pinky["turn"], Pinky["steps"], pl)
          Pinky["turn"]  = returned[0]
          Pinky["steps"] = returned[1]
          Pinky["entity"].changespeed(Pinky_directions, False, Pinky["turn"], Pinky["steps"], pl)
          Pinky["entity"].update(wall_list, False)

      for Blinky in Blinkies:
          returned = Blinky["entity"].changespeed(Blinky_directions, False, Blinky["turn"], Blinky["steps"], bl)
          Blinky["turn"]  = returned[0]
          Blinky["steps"] = returned[1]
          Blinky["entity"].changespeed(Blinky_directions, False, Blinky["turn"], Blinky["steps"], bl)
          Blinky["entity"].update(wall_list, False)

      for Inky in Inkies:
          returned = Inky["entity"].changespeed(Inky_directions, False, Inky["turn"], Inky["steps"], il)
          Inky["turn"]  = returned[0]
          Inky["steps"] = returned[1]
          Inky["entity"].changespeed(Inky_directions, False, Inky["turn"], Inky["steps"], il)
          Inky["entity"].update(wall_list, False)

      for Clyde in Clydes:
          returned = Clyde["entity"].changespeed(Clyde_directions, "clyde", Clyde["turn"], Clyde["steps"], cl)
          Clyde["turn"]  = returned[0]
          Clyde["steps"] = returned[1]
          Clyde["entity"].changespeed(Clyde_directions, "clyde", Clyde["turn"], Clyde["steps"], cl)
          Clyde["entity"].update(wall_list, False)

      # See if the Vax-Man block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Vaxman, block_list, True)
       
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(darkGrey)
        
      wall_list.draw(screen)
      gate.draw(screen)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, darkRed)
      screen.blit(text, [10, 10])

      if score == bll:
         userWantsToExit = doNext("Congratulations, you won!", 145, all_sprites_list, block_list, ghosts_list, vaxman_collide, wall_list, gate)
         if userWantsToExit:
            break

      ghosts_hit_list = pygame.sprite.spritecollide(Vaxman, ghosts_list, True)

      if ghosts_hit_list:

         for refBlinky in Blinkies:
           if refBlinky["entity"] in ghosts_hit_list:
               Blinkies = [Blinky for Blinky in Blinkies if Blinky != refBlinky]

         for refPinky in Pinkies:
           if refPinky["entity"] in ghosts_hit_list:
               Pinkies = [Pinky for Pinky in Pinkies if Pinky != refPinky]

         for refInky in Inkies:
           if refInky["entity"] in ghosts_hit_list:
               Inkies = [Inky for Inky in Inkies if Inky != refInky]

         for refClyde in Clydes:
           if refClyde["entity"] in ghosts_hit_list:
               Clydes = [Clyde for Clyde in Clydes if Clyde != refClyde]

      all_sprites_list.draw(screen)
      ghosts_list.draw(screen)

      if len(ghosts_list) >= MAXIMUM_GHOSTS:
         userWantsToExit = doNext("Game Over", 235, all_sprites_list, block_list, ghosts_list, vaxman_collide, wall_list, gate)
         if userWantsToExit:
            break

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)

def doNext(message, left, all_sprites_list, block_list, ghosts_list, vaxman_collide, wall_list, gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            return True
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del ghosts_list
            del vaxman_collide
            del wall_list
            del gate
            startGame()
            return False

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, lightGrey)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, lightGrey)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, lightGrey)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

startGame()

pygame.quit()
