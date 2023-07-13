# import time
# import winsound
#
# from detection import grab_images
# from launcher import Launcher
#
#
# def verif(zones):
#     time.sleep(3)
#     winsound.Beep(1500, 500)
#
#     l_top_img = grab_images(zones)["l_top"]
#     r_top_img = grab_images(zones)["r_top"]
#     l_mid_img = grab_images(zones)["l_mid"]
#     r_mid_img = grab_images(zones)["r_mid"]
#     l_bot_img = grab_images(zones)["l_bot"]
#     r_bot_img = grab_images(zones)["r_bot"]
#
#     l_top_img.save("../res/img/zones/top/left.png")
#     r_top_img.save("../res/img/zones/top/right.png")
#     l_mid_img.save("../res/img/zones/mid/left.png")
#     r_mid_img.save("../res/img/zones/mid/right.png")
#     l_bot_img.save("../res/img/zones/bot/left.png")
#     r_bot_img.save("../res/img/zones/bot/right.png")
#
#     winsound.Beep(1500, 250)
#
#
# def main():
#     launcher = Launcher()
#     verif(launcher.zones)
#
#
# if __name__ == "__main__":
#     main()
