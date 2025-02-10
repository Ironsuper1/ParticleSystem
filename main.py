import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, KEYDOWN, K_ESCAPE
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import sys


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

X_MIN = -3
X_MAX = 3
Y_MIN = -4
Y_MAX = 4

class particle:
    def __init__(self, position, velocity, lifetime):
        self.position = position
        self.velocity = velocity
        self.lifetime = lifetime

    def update(self, dt):
        self.position = [self.position[i] + self.velocity[i] * dt for i in range(3)]

        if self.position[0] <= X_MIN or self.position[0] >= X_MAX:
            self.velocity[0] *= -1

        if self.position[1] <= Y_MIN or self.position[1] >= Y_MAX:
            self.velocity[1] *= -1

        self.lifetime -= dt

    def is_alive(self):
        return self.lifetime > 0

class particle_system:
    def __init__(self, num_particles):
        self.particles = []
        for _ in range(num_particles):
            position = [0,0,0]
            velocity = [random.uniform(-1,1), random.uniform(1,3), random.uniform(-1,1)]
            lifetime = random.uniform(20,50)
            self.particles.append(particle(position, velocity, lifetime))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.is_alive()]

    def render(self):
        glBegin(GL_POINTS)
        for p in self.particles:
            glVertex3fv(p.position)
        glEnd()

def init_opengl():
    glEnable(GL_POINT_SMOOTH)
    glPointSize(10)
    glClearColor(0,0,0,1)

def main(num_particles):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_HEIGHT,WINDOW_WIDTH), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Particle Popsickle 9000")

    init_opengl()
    gluPerspective(45, (800/600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    
    ps = particle_system(num_particles)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ps.update(dt)
        ps.render()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    input = 100
    if len(sys.argv) > 1:
        input = int(sys.argv[1])
        print(f"Number of Particles set to: {input}")
    else:
        print("Using Default Number of Particles: 100")

    main(input)
