import pygame
from utils import constants

class Button:
    def __init__(self, x, y, width, height, status, normal_img, hover_img, click_img):
        # Initialize the button rect
        self.__rect = pygame.Rect(x, y, width, height)
        # Set the button's position and size
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        # Status of button
        self.__status = status
        # Get the normal image of button
        self.__normal_img = normal_img
        # Get the hover image of button
        self.__hover_img = hover_img
        # Get the click image of button
        self.__click_img = click_img

    # getters
    def get_status(self):
        return self.__status

    # setters
    def set_status(self, status):
        self.__status = status

    def zoom_in(self):
        # Calculate the new width and height based on zoom factor
        new_width = int(self.__width * (1 + constants.ZOOM_IN))
        new_height = int(self.__height * (1 + constants.ZOOM_IN))
        # Calculate the new position (x, y) to keep the button centered
        new_x = self.__x - (new_width - self.__width) / 2
        new_y = self.__y - (new_height - self.__height) / 2
        # Return the new position and size
        return new_width, new_height, new_x, new_y

    # Draw button on the menu
    def draw(self, surface):
        # If the button is in its normal status (0)
        if self.__status == 0:
            # Scale the normal image
            self.__normal_img = pygame.transform.scale(self.__normal_img, (self.__width, self.__height)).convert_alpha()
            # Draw the normal image on the surface
            surface.blit(self.__normal_img, self.__rect)
        # If the button is in its hover status (0)
        elif self.__status == 1:
            # Calculate the new zoomed-in position and size
            new_width, new_height, new_x, new_y = self.zoom_in()
            # Create a new rect
            hover_rect = pygame.Rect(new_x, new_y, new_width, new_height)
            # Scale the hover image
            self.__hover_img = pygame.transform.scale(self.__hover_img, (new_width, new_height)).convert_alpha()
            # Draw the hover image on the surface
            surface.blit(self.__hover_img, hover_rect)
        # If the button is clicked (2)
        elif self.__status == 2:
            # Calculate the new zoomed-in position and size
            new_width, new_height, new_x, new_y = self.zoom_in()
            # Create a new rect
            click_rect = pygame.Rect(new_x, new_y, new_width, new_height)
            # Scale the click image
            self.__click_img = pygame.transform.scale(self.__click_img, (new_width, new_height)).convert_alpha()
            # Draw the click image on the surface
            surface.blit(self.__click_img, click_rect)

    def is_hover_on(self, pos):
        # Check if the mouse is hover on the button
        return self.__rect.collidepoint(pos)