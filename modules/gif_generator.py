import datetime
from modules.async_client import AsyncClient
from modules.lobby_data import DiscordChannel
from modules.splatoon_rotation import SplatoonRotation
from modules.execute import render_gif


async def generate_gif(rotation_info: SplatoonRotation, ctx):

    # Making sure we have images to put together
    if rotation_info is None or rotation_info.stage_a_image is None or rotation_info.stage_b_image is None:
        raise AttributeError("Files to generate gif does not exist")

    # setting up the image name and image/gif file names
    image_a = rotation_info.stage_a_image
    image_b = rotation_info.stage_b_image

    # image name format: <year>-<month>-<date>-<hour>-<min>-<sec>-<channel-id>
    image_base = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "-" + str(DiscordChannel(ctx.channel).id)
    image_a_filename = image_base + "-1.png"
    image_b_filename = image_base + "-2.png"
    gif_filename = image_base + ".gif"

    # getting the images and saving them locally
    client = AsyncClient(user_agent="SplatBot/1.0 Github: github.com/ktraw2/SplatBot")
    await client.send_image_request(image_url=image_a, file_path=image_a_filename)
    await client.send_image_request(image_url=image_b, file_path=image_b_filename)

    # making the gif
    await render_gif(image_base, gif_filename)

    return gif_filename