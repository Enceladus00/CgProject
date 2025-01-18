import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Işıklandırma pozisyon/yönü / Lighting position/direction 
ambient_light_pos = [0.0, 5.0, 0.0, 1.0]
point_light_pos = [2.0, 3.0, -1.0, 1.5]
directional_light_dir = [0.0, 1.0, 0.0, 0.0]


camera_pos = [-1.0, 0.5, 2.0] 
camera_rot = [0.0, 0.0]  
mouse_sensitivity = 0.1
movement_speed = 0.1


def setup_lighting():
    
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    # Sırasıyla Ortam(Ambient), Nokta(Point) ve Yönlü(Directional) Işık./Ambient, Point and Directional Light respectively.
    # Aktive/deaktive etmek için line'ı # ile yorum satırı haline getirin./Turn the line into a comment line with # to activate/deactivate.
    glEnable(GL_LIGHT0) 
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    
    glLightfv(GL_LIGHT0, GL_POSITION, ambient_light_pos)
    
    # Ortam Işığı (Light0)
    ambient = [0.1, 0.1, 0.1, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    diffuse = [0.5, 0.5, 0.5, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    specular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    
    # Nokta Işık (Light1)
    glLightfv(GL_LIGHT1, GL_POSITION, point_light_pos)
    ambient1 = [0.0, 0.0, 0.0, 1.0]
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambient1)
    diffuse1 = [2.0, 0.75, 0.0, 1.0]  # Orange light
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse1)
    specular1 = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular1)

    # Yönlü Işık (Light2)
    glLightfv(GL_LIGHT2, GL_POSITION, directional_light_dir)
    ambient2 = [0.4, 0.4, 0.4, 1.0]
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambient2)
    diffuse2 = [0.0, 0.0, 1.5, 1.0]
    glLightfv(GL_LIGHT2, GL_DIFFUSE, diffuse2)
    specular2 = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT2, GL_SPECULAR, specular2)

    # Enable color material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def draw_light():
    glPushMatrix()
    
    glTranslatef(*point_light_pos[:3])
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 0.5, 0.0)  # Orange
    draw_sphere(0.1, 16, 16)
    glEnable(GL_LIGHTING)


    
    glPopMatrix()    

def draw_sphere(radius, slices, stacks):
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)

def draw_cube():
    subdivisions = 16
    step = 1.0 / subdivisions
    half_size = 0.5
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 25) #Parlak Yüzey/ Shiny Surface
    faces = [
        {'normal': (0, 0, 1), 'start': (-half_size, -half_size, half_size), 'u': (1, 0, 0), 'v': (0, 1, 0)},
        {'normal': (0, 0, -1), 'start': (half_size, -half_size, -half_size), 'u': (-1, 0, 0), 'v': (0, 1, 0)},
        {'normal': (-1, 0, 0), 'start': (-half_size, -half_size, -half_size), 'u': (0, 0, 1), 'v': (0, 1, 0)},
        {'normal': (1, 0, 0), 'start': (half_size, -half_size, half_size), 'u': (0, 0, -1), 'v': (0, 1, 0)},
        {'normal': (0, 1, 0), 'start': (-half_size, half_size, -half_size), 'u': (1, 0, 0), 'v': (0, 0, 1)},
        {'normal': (0, -1, 0), 'start': (-half_size, -half_size, half_size), 'u': (1, 0, 0), 'v': (0, 0, -1)},
    ]
    for face in faces:
        glBegin(GL_QUADS)
        glNormal3f(*face['normal'])
        for i in range(subdivisions):
            for j in range(subdivisions):
                s = i * step
                t = j * step
                s_next = s + step
                t_next = t + step

                # Compute vertices
                v0 = (
                    face['start'][0] + s * face['u'][0] + t * face['v'][0],
                    face['start'][1] + s * face['u'][1] + t * face['v'][1],
                    face['start'][2] + s * face['u'][2] + t * face['v'][2]
                )
                v1 = (
                    face['start'][0] + s_next * face['u'][0] + t * face['v'][0],
                    face['start'][1] + s_next * face['u'][1] + t * face['v'][1],
                    face['start'][2] + s_next * face['u'][2] + t * face['v'][2]
                )
                v2 = (
                    face['start'][0] + s_next * face['u'][0] + t_next * face['v'][0],
                    face['start'][1] + s_next * face['u'][1] + t_next * face['v'][1],
                    face['start'][2] + s_next * face['u'][2] + t_next * face['v'][2]
                )
                v3 = (
                    face['start'][0] + s * face['u'][0] + t_next * face['v'][0],
                    face['start'][1] + s * face['u'][1] + t_next * face['v'][1],
                    face['start'][2] + s * face['u'][2] + t_next * face['v'][2]
                )

                # Compute normals for each vertex (same as face normal for cube)
                glNormal3f(*face['normal'])

                glVertex3f(*v0)
                glVertex3f(*v1)
                glVertex3f(*v2)
                glVertex3f(*v3)
        glEnd()

def draw_room():
    size = 10  # Half-dimension of the room
    glBegin(GL_QUADS)
    
    # Floor
    glNormal3f(0.0, 1.0, 0.0)  # Upward normal
    glColor3f(0.5, 0.5, 0.5)  # Gray color
    glVertex3f(-size, -1, -size)
    glVertex3f(size, -1, -size)
    glVertex3f(size, -1, size)
    glVertex3f(-size, -1, size)
    
    # Ceiling
    glNormal3f(0.0, -1.0, 0.0)  # Downward normal
    glColor3f(0.8, 0.8, 0.8)  # Light gray
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    
    # Back Wall
    glNormal3f(0.0, 0.0, 1.0)  # Forward normal
    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)
    
    # Front Wall
    glNormal3f(0.0, 0.0, -1.0)  # Backward normal
    glColor3f(0.6, 0.6, 0.6)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    
    # Left Wall
    glNormal3f(1.0, 0.0, 0.0)  # Right normal
    glColor3f(0.4, 0.4, 0.4)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, size, -size)
    
    # Right Wall
    glNormal3f(-1.0, 0.0, 0.0)  # Left normal
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    
    glEnd()

def draw_pyramid():
    vertices = [
        [0, 1, 0], [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1]
    ]
    faces = [
        (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1),
        (1, 2, 3), (1, 3, 4)
    ]

    mat_ambient = [0.7, 0.7, 0.7, 1.0]
    mat_diffuse = [0.8, 0.8, 0.8, 1.0]
    mat_specular = [0.0, 0.0, 0.0, 1.0]
    mat_shininess = [0.0]                   #mat yüzey/Matte surface

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)

    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()



# Camera movement
def handle_input():
    global camera_pos, camera_rot

    keys = pygame.key.get_pressed()
    mouse_movement = pygame.mouse.get_rel()

    
    camera_rot[0] -= mouse_movement[1] * mouse_sensitivity  # X rotasyonu
    camera_rot[1] -= mouse_movement[0] * mouse_sensitivity  # Y rotasyonu

    #(WASD or arrow keys)
    direction = np.array([
        np.sin(np.radians(camera_rot[1])),
        0,
        np.cos(np.radians(camera_rot[1]))
    ])
    right = np.array([
        np.cos(np.radians(camera_rot[1])),
        0,
        -np.sin(np.radians(camera_rot[1]))
    ])
    if keys[K_s]:
        camera_pos += direction * movement_speed
    if keys[K_w]:
        camera_pos -= direction * movement_speed
    if keys[K_a]:
        camera_pos -= right * movement_speed
    if keys[K_d]:
        camera_pos += right * movement_speed
    if keys[K_LSHIFT]:
        camera_pos[1] += movement_speed
    if keys[K_LCTRL]:
        camera_pos[1] -= movement_speed
    if keys[K_ESCAPE]: # Çıkış
        pygame.quit()
        quit()


def update_camera():
    glRotatef(-camera_rot[0], 1, 0, 0) 
    glRotatef(-camera_rot[1], 0, 1, 0)
    glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2]) 


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    
    update_camera()

    draw_room()
    draw_light()

    glColor3f(1, 0.3, 0.3)
    glTranslatef(-2, 0, -5)
    draw_cube()

    glColor3f(0.3, 1, 0.3)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.3, 1.0, 0.3, 1.0])
    glTranslatef(4, 0, 0)
    draw_sphere(1, 256, 256)

    glColor3f(1, 1, 1)
    glTranslatef(0, 0, 4)
    draw_sphere(.5, 128, 128)

    glColor3f(1, 1, 0.3)
    glTranslatef(-2, 0, 5)
    draw_pyramid()

    glPopMatrix()
    pygame.display.flip()


#game loop
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)  
    glEnable(GL_DEPTH_TEST)     
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True) 
    setup_lighting()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        handle_input()
        draw_scene()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
