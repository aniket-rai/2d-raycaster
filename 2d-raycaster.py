# 2d ray caster made in pygame
import pygame
import sys
import math


# Class for light particle and corresponding light rays
class Particle:
    def __init__(self, screen, colour):
        self.screen = screen
        self.colour = colour
        self.radius = 2000 
    
    def draw(self, centre, objects):
        pygame.draw.circle(self.screen, self.colour, centre, 3)
        
        for i in range(0, 360):
            points = []
            dist = []

            # calculate outer radii coordinates for ray building
            centre_2 = [self.radius * math.cos(i) + centre[0], self.radius * math.sin(i) + centre[1]]
            
            # get collision data
            for obj in objects:
                points = points + obj.collision(centre, centre_2)
                    
            # calculate the distances from centre to each collision point
            for point in points:
                distance = math.sqrt((centre[0] - point[0])**2 + (centre[1] - point[1])**2)
                dist.append(distance)
            
            # pick the point with the minimum distance
            pt2 = points[dist.index(min(dist))]

            # draw rays
            #if (0 <= pt2[0] <= 1080 or 0 <= pt2[1] <= 720):
            pygame.draw.aaline(self.screen, self.colour, centre, pt2, 2)

 
# Class for lines to be used as boundaries
class Boundary:
    def __init__(self, screen, pt1, pt2, width):
        self.screen = screen
        self.pt1 = pt1
        self.pt2 = pt2
        self.width = width
    
    def draw(self):
        pygame.draw.aaline(self.screen, [255,255,0], self.pt1, self.pt2, self.width)
    
    def collision(self, centre, centre_2):
        x1, y1 = centre
        x2, y2 = centre_2
        x3, y3 = self.pt1
        x4, y4 = self.pt2

        denom = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))

        # avoid 0 error
        if (denom == 0):
            return [tuple(centre_2)]

        # use vector math to calculate if lines intersect (dot product)
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/denom
        u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/denom

        # first degree Bezier parameters that accommodate a fixed line segment
        if (t >= 0 and t <= 1 and u >= 0 and u <= 1):
            pt2 = [x1+t*(x2-x1), y1+t*(y2-y1)]
        else:
            pt2 = centre_2

        return [tuple(pt2)]


class Circle:
    def __init__(self, screen, centre, radius, width):
        self.screen = screen
        self.colour = [255, 0, 255]
        self.centre = centre
        self.radius = radius
        self.width = width

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, self.centre, self.radius, self.width)

    def collision(self, centre, centre_2):
        Q = pygame.math.Vector2(self.centre)
        r = self.radius
        A = pygame.math.Vector2(centre)
        B = pygame.math.Vector2(centre_2)
        points = []

        V = B - A

        # using vector formulae for distance from line to a point (centre of circle)
        # vector line formula: A + tN
        # disc > 0 -> 2 sols, disc = 0 -> 1 sol, disc < 0 -> 0 sols
        a = V.dot(V)
        b = 2 * V.dot(A - Q)
        c = A.dot(A) + Q.dot(Q) - 2 * A.dot(Q) - r**2

        disc = b**2 - 4 * a * c

        # check if any solutions exist
        if disc < 0:
            point = centre_2
        else:
            t1 = (-b + math.sqrt(disc))/(2*a)
            t2 = (-b - math.sqrt(disc))/(2*a)
            
            # check if solution within limits (line segment) exists
            if (0 <= t1 <= 1):
                t = t1
                points.append(A + t*V)
            else:
                points.append(centre_2)

            if (0 <= t2 <= 1):
                t = t2
                points.append(A + t*V)
            else:
                points.append(centre_2)
        
        return points

def main():
    pygame.init()

    size = 1080, 720

    black = 20,20,20
    white = 255,255,255
    red = 255,0,0
    green = 0,255,0
    blue = 0,0,255

    objects = []

    screen = pygame.display.set_mode(size)

    particle = Particle(screen, white)
    boundary1 = Boundary(screen, [700, 400], [700, 500], 4)
    boundary2 = Boundary(screen, [200, 400], [700, 400], 4)
    boundary3 = Boundary(screen, [200, 400], [200, 500], 4)
    boundary4 = Boundary(screen, [200, 500], [700, 500], 4)
    boundary5 = Boundary(screen, [454, 100],  [918, 88], 4)
    boundary6 = Boundary(screen, [300, 145], [873, 10], 4)

    circle1 = Circle(screen, [900,600], 50, 2)
    circle2 = Circle(screen, [100,100], 100, 2)

    objects.append(boundary1)
    objects.append(boundary2)
    objects.append(boundary3)
    objects.append(boundary4)
    objects.append(boundary5)
    objects.append(circle1)
    objects.append(circle2)
    objects.append(boundary6)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        screen.fill(black)

        centre = pygame.mouse.get_pos()

        for obj in objects:
            obj.draw()
        
        particle.draw(centre, objects)
        pygame.display.flip()

main()