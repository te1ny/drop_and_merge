import math
import pygame

def simulate_physics(balls, gravity, friction, basket, dt=1, iterations=6, additional_radius=15, merge_sound=None, collision_sound=None):
    total_merged = 0
    for ball in balls:
        ball.velocity[1] += gravity * dt
        ball.position[0] += ball.velocity[0] * dt
        ball.position[1] += ball.velocity[1] * dt
        ball.velocity[0] *= friction
        ball.velocity[1] *= friction

    for _ in range(iterations):
        merge_list = []
        merged_indices = set()
        n = len(balls)
        for i in range(n):
            for j in range(i+1, n):
                if i in merged_indices or j in merged_indices:
                    continue
                b1 = balls[i]
                b2 = balls[j]
                dx = b2.position[0] - b1.position[0]
                dy = b2.position[1] - b1.position[1]
                distance = math.hypot(dx, dy)
                if distance == 0:
                    continue
                overlap = b1.radius + b2.radius - distance
                if overlap > 0:
                    if b1.radius == b2.radius:
                        new_radius = b1.radius + additional_radius
                        avg_x = (b1.position[0] + b2.position[0]) / 2
                        avg_y = (b1.position[1] + b2.position[1]) / 2
                        merged_ball = type(b1)((avg_x, avg_y), new_radius, b1.is_image, b1.ball_dict)
                        merged_ball.velocity[0] = (b1.velocity[0] + b2.velocity[0]) / 2
                        merged_ball.velocity[1] = (b1.velocity[1] + b2.velocity[1]) / 2
                        merged_ball.update_image()
                        merged_indices.add(i)
                        merged_indices.add(j)
                        merge_list.append(merged_ball)
                        total_merged += 1
                        if merge_sound:
                            merge_sound.play()
                    else:
                        nx = dx / distance
                        ny = dy / distance
                        rel_vel = (b2.velocity[0] - b1.velocity[0]) * nx + (b2.velocity[1] - b1.velocity[1]) * ny
                        e = 1.0
                        inv_mass1 = 1 / b1.mass
                        inv_mass2 = 1 / b2.mass
                        denom = inv_mass1 + inv_mass2
                        impulse = -(1 + e) * rel_vel / (denom if denom != 0 else 1)
                        b1.velocity[0] -= impulse * nx * inv_mass1
                        b1.velocity[1] -= impulse * ny * inv_mass1
                        b2.velocity[0] += impulse * nx * inv_mass2
                        b2.velocity[1] += impulse * ny * inv_mass2
                        percent = 0.8
                        correction = (overlap * percent) / (denom if denom != 0 else 1)
                        b1.position[0] -= nx * correction * inv_mass1
                        b1.position[1] -= ny * correction * inv_mass1
                        b2.position[0] += nx * correction * inv_mass2
                        b2.position[1] += ny * correction * inv_mass2
                        if collision_sound and abs(rel_vel) > 0.1:
                            collision_sound.play()
        if merged_indices:
            new_balls = [balls[i] for i in range(n) if i not in merged_indices]
            new_balls.extend(merge_list)
            balls = new_balls

        if basket is not None:
            for ball in balls:
                resolve_circle_rect(ball, basket.left_boundary)
                resolve_circle_rect(ball, basket.right_boundary)
                resolve_circle_rect(ball, basket.bottom_boundary)

    return balls, total_merged

def resolve_collisions(balls, additional_radius, merge_sound=None, collision_sound=None):
    return simulate_physics(balls, gravity=0, friction=1, basket=None, dt=0, iterations=1, additional_radius=additional_radius, merge_sound=merge_sound, collision_sound=collision_sound)

def resolve_circle_rect(ball, rect):
    cx, cy = ball.position
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    dist = math.hypot(dx, dy)

    if dist < ball.radius:
        penetration = ball.radius - dist

        if dist != 0:
            nx = dx / dist
            ny = dy / dist
        else:
            nx, ny = 0, -1

        ball.position[0] += nx * penetration
        ball.position[1] += ny * penetration
        vel_dot_n = ball.velocity[0] * nx + ball.velocity[1] * ny

        if vel_dot_n < 0:
            ball.velocity[0] -= vel_dot_n * nx
            ball.velocity[1] -= vel_dot_n * ny
