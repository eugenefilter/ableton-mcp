import re

def srt_time_to_seconds(time_str):
    h, m, s_ms = time_str.split(':')
    s, ms = s_ms.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def parse_srt_to_sql(srt_content):
    sql_commands = []
    # Add video entry and get its ID
    sql_commands.append("INSERT INTO videos (url, language, duration_s, status) VALUES ('https://www.youtube.com/watch?v=LDSUPQNbueE', 'en', 1026, 'ingested') RETURNING id;")

    # Process segments
    # In a real script, you'd fetch the returned id. For this script, we'll assume it's 1.
    video_id = 1

    # Split content into blocks based on double newlines
    # The file uses \r\n, so we split on that sequence repeated.
    blocks = srt_content.strip().split('\r\n\r\n')

    for block in blocks:
        lines = block.split('\r\n')
        # A valid block has at least 3 lines: index, timestamp, text
        if len(lines) >= 3:
            try:
                time_line = lines[1]
                text_lines = lines[2:]

                start_str, end_str = [t.strip() for t in time_line.split('-->')]
                start_s = srt_time_to_seconds(start_str)
                end_s = srt_time_to_seconds(end_str)

                # Join potentially multiple lines of text and escape single quotes
                transcript = " ".join(text_lines).replace("'", "''").strip()

                if transcript:  # Ensure there is text to insert
                    sql = f"INSERT INTO video_segments (video_id, start_s, end_s, transcript_fragment) VALUES ({video_id}, {start_s:.3f}, {end_s:.3f}, '{transcript}');"
                    sql_commands.append(sql)
            except (ValueError, IndexError):
                # Skip malformed blocks
                continue

    return "\n".join(sql_commands)

# Read the SRT file
with open('/Users/eugene/Documents/Ableton/app/lessons/Intro Into Making Amen Jungle Breaks in Ableton [English (auto-generated)] [DownloadYoutubeSubtitles.com].srt', 'r') as f:
    srt_file_content = f.read()

# Clean up the SRT content (remove the first two lines which are not part of the SRT spec)
cleaned_srt = '\r\n'.join(srt_file_content.split('\r\n')[2:])

# Generate the SQL
sql_script_content = parse_srt_to_sql(cleaned_srt)

# Write the SQL to a file
with open('/Users/eugene/Documents/Ableton/app/ingest.sql', 'w') as f:
    f.write(sql_script_content)

print("ingest.sql file generated successfully.")
