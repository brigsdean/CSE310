"""
Forest Maze

This program will run a simple maze game wherein the player needs to collect
some firewood for a campout in a maze of trees.
"""

import arcade

# constants
WINDOW_SIDE = 1024 # the window is a square
WINDOW_TITLE = "Forest Maze"
PLAYER_UP = 0
PLAYER_DOWN = 1
PLAYER_RIGHT = 2
PLAYER_LEFT = 3
PLAYER_SPEED = 2

"""
Player

Defines the player character. 
"""
class Player(arcade.Sprite):
    # set up default parameters
    def __init__(self):
        super().__init__()

        # put the player sprites into a list 
        self.sprites = []
        texture = arcade.load_texture("sprites/player_up.png")
        self.sprites.append(texture)
        texture = arcade.load_texture("sprites/player_down.png")
        self.sprites.append(texture)
        texture = arcade.load_texture("sprites/player_right.png")
        self.sprites.append(texture)
        texture = arcade.load_texture("sprites/player_left.png")
        self.sprites.append(texture)
        self.texture = texture # start by looking left 

    def update(self):
        # allow the player to move 
        self.center_x += self.change_x
        self.center_y += self.change_y

        # when the player changes directions, update which sprite is used 
        if self.change_y > 0:
            self.texture = self.sprites[PLAYER_UP]
        elif self.change_y < 0:
            self.texture = self.sprites[PLAYER_DOWN]
        elif self.change_x < 0:
            self.texture = self.sprites[PLAYER_LEFT]
        elif self.change_x > 0:
            self.texture = self.sprites[PLAYER_RIGHT]


"""
Tree Maze

The main body of the program.
"""
class TreeMaze(arcade.Window):

    # Anitializes the game
    def __init__(self):
        # give it the parameters it needs
        super().__init__(WINDOW_SIDE, WINDOW_SIDE, WINDOW_TITLE)

        # set the score
        self.score = 0

        # set a background for the window
        self.ground = None

        # set up sprite lists
        self.branch_list = []
        self.trees_list = []
        self.camp_list = []
        self.collision_list = []
        self.entity_list = []

    # Allows the game to be reset without exiting the program 
    def setup(self):
        # set up background music
        self.music = arcade.Sound(":resources:music/funkyrobot.mp3", True)
        self.music.play(0.25)

        # set up sprite lists 
        self.branch_list = arcade.SpriteList()
        self.trees_list = arcade.SpriteList()
        self.camp_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()
        self.entity_list = arcade.SpriteList()

        # Because of how the maze is rendered, I'm using a custom coordinate, 
        # or "cc", to convert the user-friendly (x, y) coordinate to what the
        # game uses to place sprites. For example, (0, 0) would turn into
        # (32, 32), and (15, 15) becomes (992, 992). 
        cc = lambda c : 32 + (64 * c)

        # set up background
        self.ground = arcade.load_texture("sprites/ground.png")

        # set up the camp
        self.campfire = arcade.Sprite("sprites/campfire_off.png")
        self.campfire.center_x = cc(13)
        self.campfire.center_y = cc(2)
        self.camp_list.append(self.campfire)

        self.tent = arcade.Sprite("sprites/tent.png")
        self.tent.center_x = cc(14)
        self.tent.center_y = cc(3)
        self.camp_list.append(self.tent)

        # add the camp to the collision list
        self.collision_list.extend(self.camp_list)

        # set up the player 
        self.player = Player()
        self.player.center_x = self.width * 0.9
        self.player.center_y = self.height * 0.1
        self.entity_list.append(self.player)

        # set up the branches
        branch_coordinate_list = [[1, 2], [1, 8], [4, 12], [7, 1], [9, 1], 
        [12, 4], [14, 5], [14, 8], [9, 5], [7, 8], [3, 10], [12, 14], [14, 10],
        [ 14, 14], [8, 14], [5, 4]]

        for coord in branch_coordinate_list:
            # create a branch with the right texture
            branch = arcade.Sprite("sprites/branch.png")

            # convert our coordinates into something the game can use
            coord[0] = cc(coord[0])
            coord[1] = cc(coord[1])
            branch.position = coord

            # put the new branch onto the list 
            self.branch_list.append(branch)

        # add the branches to the entity list
        self.entity_list.extend(self.branch_list)

        # set up the trees
        tree_coordinate_list = []

        # the tree border
        for x in range(16):
            tree_coordinate_list.append([0, x])
            tree_coordinate_list.append([x, 0])
            tree_coordinate_list.append([15, x])
            tree_coordinate_list.append([x, 15])

        # all of the other trees in the maze... yep
        tree_maze_list = [[1, 3],  [1, 7], [2, 2], [2, 3], [2, 5], [2, 7], 
        [2, 8], [2, 9], [2, 10], [2, 12], [2, 13], [3, 5], [3, 9], [3, 13],
        [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 9], [4, 10],
        [4, 11], [4, 13], [5, 7], [5, 11], [5, 12], [5, 13], [6, 2], [6, 3], 
        [6, 4], [6, 5], [6, 7], [6, 8], [6, 9], [7, 2], [7, 7], [7, 9], 
        [7, 11], [7, 12], [7, 13], [8, 1], [8, 2], [8, 4], [8, 5], [8, 6], 
        [8, 7], [8, 9], [8, 13], [9, 2], [9, 4], [9, 9], [9, 10], [9, 11], 
        [9, 13], [9, 14], [10, 4], [10, 5], [10, 7], [10, 11], [11, 1], 
        [11, 2], [11, 5], [11, 7], [11, 8], [11, 9], [11, 13], [12, 5], 
        [12, 9], [12, 11], [12, 12], [12, 13], [13, 4], [13, 5], [13, 7], 
        [13, 9], [13, 13], [13, 14], [14, 4], [14, 7], [14, 9], [14, 11]]

        # combine the two lists
        tree_coordinate_list.extend(tree_maze_list)

        # add them all to the tree list
        for coord in tree_coordinate_list:
            # get the tree sprite
            tree = arcade.Sprite("sprites/tree.png")

            # convert our coordinates into something the game can use
            coord[0] = cc(coord[0])
            coord[1] = cc(coord[1])
            tree.position = coord

            # put the new tree onto the list 
            self.trees_list.append(tree)

        # add the trees to the collision list
        self.collision_list.extend(self.trees_list)

    # Draws all of the objects we need
    def on_draw(self):
        # start the drawings
        arcade.start_render()

        # draw the background
        arcade.draw_lrwh_rectangle_textured(0, 0, WINDOW_SIDE, WINDOW_SIDE, 
        self.ground)
        
        # draw the player, branches, trees, and camping gear
        self.entity_list.draw()
        self.collision_list.draw() 

    # Detects when the player presses a key
    def on_key_press(self, symbol, modifiers):
        # allows player to "sprint"
        if symbol == arcade.key.LSHIFT:
            self.player.change_x *= 1.5
            self.player.change_y *= 1.5

        # up
        if symbol == arcade.key.W:
            self.player.change_y = PLAYER_SPEED

        # down
        if symbol == arcade.key.S:
            self.player.change_y = -PLAYER_SPEED

        # left
        if symbol == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED

        # right
        if symbol == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

        # quit game
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

    # Detects when a player lets go of a key 
    def on_key_release(self, symbol, modifiers):
        # sprint function
        if symbol == arcade.key.LSHIFT:
            self.player.change_x *= (2.0 / 3.0)
            self.player.change_y *= (2.0 / 3.0)

        if symbol == arcade.key.W or symbol == arcade.key.S:
            self.player.change_y = 0

        if symbol == arcade.key.A or symbol == arcade.key.D:
            self.player.change_x = 0

    # Updates all of the sprites 
    def on_update(self, delta_time: float):
        # update the player and branches 
        self.entity_list.update()

        # make a list of branches that were collected
        collected_branches = arcade.check_for_collision_with_list(self.player, 
        self.branch_list)

        # remove branches, add to the score, and make a sound
        for branch in collected_branches:
            branch.remove_from_sprite_lists()
            self.score += 1
            self.sound = arcade.Sound(":resources:sounds/coin5.wav")
            self.sound.play(0.5)
        
        # detect if the player has touched a tree or the camping equipment
        if self.player.collides_with_list(self.collision_list):
            self.player.change_x = 0
            self.player.change_y = 0

        # if a player returns to camp with at least 4 branches, they win
        if self.player.collides_with_list(self.camp_list) and self.score > 3:
            self.player.change_x = 0
            self.player.change_y = 0
            arcade.close_window()

        
"""
Main

The entry point for the program. 
"""
def main():
    window = TreeMaze()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()