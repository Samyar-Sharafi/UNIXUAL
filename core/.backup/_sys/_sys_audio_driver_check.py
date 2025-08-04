import pygame
import re

def play_song_with_lyrics( mp3_path, lrc_path ) :
    pygame.init()
    pygame.mixer.init()

    # Load lyrics
    lyrics = [ ]
    with open( lrc_path, encoding='utf-8' ) as f :
        for line in f :
            match = re.match( r'\[(\d+):(\d+\.\d+)\](.*)', line.strip() )
            if match :
                minutes = int( match.group( 1 ) )
                seconds = float( match.group( 2 ) )
                time_sec = minutes * 60 + seconds
                lyrics.append( (time_sec, match.group( 3 )) )

    lyrics.sort()

    # Load and play music
    pygame.mixer.music.load( mp3_path )
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    idx = 0

    running = True
    while running :
        # Calculate elapsed time in seconds
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000

        # Show lyrics when it's time
        while idx < len( lyrics ) and elapsed >= lyrics[ idx ][ 0 ] :
            print( lyrics[ idx ][ 1 ] )
            idx += 1


        # Check if music finished playing
        if not pygame.mixer.music.get_busy() :
            running = False

        # Limit loop to 60 frames per second (adjust as needed)
        clock.tick( 60 )

    pygame.quit()


print("damn, ur smart!")
play_song_with_lyrics( './legacy/audio_test.mp3', './legacy/lyric_test.lrc' )
