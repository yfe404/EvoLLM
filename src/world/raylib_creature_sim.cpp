
#include "raylib.h"
#include <vector>
#include <cmath>
#include <cstdlib>

struct Creature {
    Vector2 position;
    float angle;
    float energy;

    void update() {
        float speed = 1.0f;
        position.x += speed * cos(angle);
        position.y += speed * sin(angle);

        // Keep inside screen
        if (position.x < 0) position.x = 0;
        if (position.y < 0) position.y = 0;
        if (position.x > 800) position.x = 800;
        if (position.y > 600) position.y = 600;

        // Lose energy over time
        energy -= 0.1f;
    }

    void draw() const {
        DrawCircleV(position, 5, energy > 0 ? GREEN : DARKGRAY);
    }
};

int main() {
    InitWindow(800, 600, "Raylib Creature Simulation");
    SetTargetFPS(60);

    std::vector<Creature> creatures;
    for (int i = 0; i < 50; ++i) {
        creatures.push_back({(Vector2){GetRandomValue(100, 700), GetRandomValue(100, 500)},
                             GetRandomValue(0, 360) * DEG2RAD,
                             100.0f});
    }

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(BLACK);

        for (auto &c : creatures) {
            c.update();
            c.draw();
        }

        DrawText("Minimal Creature Simulation", 10, 10, 20, RAYWHITE);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
