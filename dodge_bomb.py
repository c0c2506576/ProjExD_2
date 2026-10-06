import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True

    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False

    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False

    return yoko, tate


def gameover(screen):
    over = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(over, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    over.set_alpha(200)

    over_font = pg.font.Font(None, 100)
    txt = over_font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    over.blit(txt, txt_rct)

    over_img = pg.image.load("fig/8.png")

    left_rct = over_img.get_rect(
        center=(WIDTH // 2 - 350, HEIGHT // 2)
    )
    over.blit(over_img, left_rct)

    right_rct = over_img.get_rect(
        center=(WIDTH // 2 + 350, HEIGHT // 2)
    )
    over.blit(over_img, right_rct)

    screen.blit(over, (0, 0))
    pg.display.update()

    time.sleep(5)


def get_kk_imgs():
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)

    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (0, -5): pg.transform.rotozoom(kk_img, 90, 1.0),
        (0, 5): pg.transform.rotozoom(kk_img, -90, 1.0),
        (5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 180, 1.0),
        (5, -5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, 135, 1.0),
        (-5, 5): pg.transform.rotozoom(kk_img, -135, 1.0),
        (5, 5): pg.transform.rotozoom(kk_img, -45, 1.0),
    }

    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # キーと移動量の対応
    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0),
    }

    bg_img = pg.image.load("fig/pg_bg.jpg")

    # こうかとんの画像を取得
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]

    # こうかとんの位置
    kk_rct = kk_img.get_rect()
    kk_rct.center = WIDTH // 2, HEIGHT // 2 + 80

    # 爆弾
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)

    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(10, WIDTH - 10)
    bb_rct.centery = random.randint(10, HEIGHT - 10)

    vx = 5
    vy = 5

    clock = pg.time.Clock()

    while True:

        # イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # キー入力
        key_lst = pg.key.get_pressed()

        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # こうかとんの向きを変更
        kk_img = kk_imgs[tuple(sum_mv)]

        # 画像が変わっても中心位置を維持
        center = kk_rct.center
        kk_rct = kk_img.get_rect(center=center)

        # こうかとんを移動
        kk_rct.move_ip(sum_mv)

        # 画面外に出ないようにする
        if not all(check_bound(kk_rct)):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 爆弾を移動
        bb_rct.move_ip(vx, vy)

        yoko, tate = check_bound(bb_rct)

        if not yoko:
            vx *= -1

        if not tate:
            vy *= -1

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # 画面描画
        screen.blit(bg_img, (0, 0))
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()