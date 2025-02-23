#build a simulation of the 3 body problem in 3D in python
# use the Euler method to solve the equations of motion
# use the Runge-Kutta method to solve the equations of motion
# use the Verlet method to solve the equations of motion
# use the symplectic Euler method to solve the equations of motion
# use the symplectic Runge-Kutta method to solve the equations of motion
# use the symplectic Verlet method to solve the equations of motion
# use the symplectic symplectic Euler method to solve the equations of motion
# display the simulation in 3D in real time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Gravitational constant
G = 6.67430e-11  # m^3 kg^-1 s^-2 (scaled for simulation)

# Body class to store position, velocity, and mass
class Body:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)

# Compute gravitational acceleration between bodies
def compute_acceleration(bodies):
    n = len(bodies)
    acc = [np.zeros(3) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                r = bodies[j].pos - bodies[i].pos
                dist = np.linalg.norm(r)
                if dist > 0:  # Avoid division by zero
                    acc[i] += G * bodies[j].mass * r / dist**3
    return acc

# Euler method
def euler_step(bodies, dt):
    acc = compute_acceleration(bodies)
    for i, body in enumerate(bodies):
        body.vel += acc[i] * dt
        body.pos += body.vel * dt

# Runge-Kutta 4 method
def rk4_step(bodies, dt):
    n = len(bodies)
    pos0 = [body.pos.copy() for body in bodies]
    vel0 = [body.vel.copy() for body in bodies]
    
    # k1: initial derivatives
    acc1 = compute_acceleration(bodies)
    k1_pos = [vel0[i] for i in range(n)]
    k1_vel = acc1
    
    # k2: midpoint at dt/2
    for i, body in enumerate(bodies):
        body.pos = pos0[i] + 0.5 * dt * k1_pos[i]
        body.vel = vel0[i] + 0.5 * dt * k1_vel[i]
    acc2 = compute_acceleration(bodies)
    k2_pos = [body.vel for body in bodies]
    k2_vel = acc2
    
    # k3: midpoint at dt/2 with k2
    for i, body in enumerate(bodies):
        body.pos = pos0[i] + 0.5 * dt * k2_pos[i]
        body.vel = vel0[i] + 0.5 * dt * k2_vel[i]
    acc3 = compute_acceleration(bodies)
    k3_pos = [body.vel for body in bodies]
    k3_vel = acc3
    
    # k4: full step
    for i, body in enumerate(bodies):
        body.pos = pos0[i] + dt * k3_pos[i]
        body.vel = vel0[i] + dt * k3_vel[i]
    acc4 = compute_acceleration(bodies)
    k4_pos = [body.vel for body in bodies]
    k4_vel = acc4
    
    # Update positions and velocities
    for i, body in enumerate(bodies):
        body.pos = pos0[i] + (dt / 6.0) * (k1_pos[i] + 2*k2_pos[i] + 2*k3_pos[i] + k4_pos[i])
        body.vel = vel0[i] + (dt / 6.0) * (k1_vel[i] + 2*k2_vel[i] + 2*k3_vel[i] + k4_vel[i])

# Verlet method (velocity Verlet)
def verlet_step(bodies, dt):
    acc = compute_acceleration(bodies)
    for i, body in enumerate(bodies):
        body.pos += body.vel * dt + 0.5 * acc[i] * dt**2
    acc_new = compute_acceleration(bodies)
    for i, body in enumerate(bodies):
        body.vel += 0.5 * (acc[i] + acc_new[i]) * dt

# Symplectic Euler method
def symplectic_euler_step(bodies, dt):
    acc = compute_acceleration(bodies)
    for i, body in enumerate(bodies):
        body.vel += acc[i] * dt
        body.pos += body.vel * dt

# Initialize three bodies with random positions and velocities
np.random.seed(42)  # For reproducibility
bodies = [
    Body(1e10, [np.random.uniform(-10, 10) for _ in range(3)], [np.random.uniform(-0.1, 0.1) for _ in range(3)]),
    Body(1e10, [np.random.uniform(-10, 10) for _ in range(3)], [np.random.uniform(-0.1, 0.1) for _ in range(3)]),
    Body(1e10, [np.random.uniform(-10, 10) for _ in range(3)], [np.random.uniform(-0.1, 0.1) for _ in range(3)])
]

# Set up 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()  # Interactive mode for real-time updates

# Simulation parameters
dt = 0.5  # Increased time step for faster motion
steps = 1000

# Main simulation loop
for step in range(steps):
    # Choose a method by uncommenting one (default: RK4)
    # euler_step(bodies, dt)
    rk4_step(bodies, dt)  # Using RK4 as it’s stable with larger dt
    # verlet_step(bodies, dt)
    # symplectic_euler_step(bodies, dt)
    
    # Clear previous plot
    ax.cla()
    
    # Plot current positions
    for i, body in enumerate(bodies):
        ax.scatter(body.pos[0], body.pos[1], body.pos[2], label=f'Body {i+1}')
    
    # Set plot limits and labels
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    
    # Update plot
    plt.draw()
    plt.pause(0.001)  # Reduced pause for faster rendering

plt.ioff()  # Turn off interactive mode
plt.show()