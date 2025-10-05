from untils import generate_video_by_image_ffmpeg, get_media_duration

duration = get_media_duration('./public/ad_videos/ad1.mkv')
print(duration)
generate_video_by_image_ffmpeg('./public/ad_videos/ad1.mkv', './videos/ad_draff.mkv', duration, './public/decorates/decorate1/persons/person_1.png', './public/decorates/decorate1/avatar.png' )