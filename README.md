# srt-duplicate-line-merger

## Usage

Place script into directory containing the srt files to be modified. Run

`python3 duplicate_line_merger.py`

Consolidated files will be populated in the 'merged' directory

## Example

Subtitles will sometimes have the same line split into multiple time signatures

```
4
00:00:54,805 --> 00:00:55,847
Who's available?

5
00:00:56,223 --> 00:00:56,557
We have word that Lightning Max
and Smile Man are on their way.

6
00:00:56,557 --> 00:00:56,890
We have word that Lightning Max
and Smile Man are on their way.

7
00:00:56,890 --> 00:00:57,224
We have word that Lightning Max
and Smile Man are on their way.

8
00:00:57,224 --> 00:00:57,558
We have word that Lightning Max
and Smile Man are on their way.

9
00:00:57,558 --> 00:00:57,891
We have word that Lightning Max
and Smile Man are on their way.

10
00:00:57,891 --> 00:00:58,225
We have word that Lightning Max
and Smile Man are on their way.

11
00:00:58,226 --> 00:01:00,036
We have word that Lightning Max
and Smile Man are on their way.

12
00:01:00,060 --> 00:01:00,394
Get me that threat level assessment!
```

Consolidated subtitles:

```
4
00:00:54,805 --> 00:00:55,847
Who's available?

5
00:00:56,223 --> 00:01:00,036
We have word that Lightning Max
and Smile Man are on their way.

6
00:01:00,060 --> 00:01:02,168
Get me that threat level assessment!

```
