# AudioNFT
A new way to create NFTs by combining audio and image collections

Mp3 files must have the following name format:
Artist - Song Title.mp3
Ex: DJCatskillNFT - Speedy-go-go.mp3
Ex: Herr Doktor - Can You Kiss Me First.mp3
Tech Notes:
This program looks for " - " as a separator between Artist and Song Title.
This program will split the Artist section by " " and search Artist[0]for an integer. 
That integer will be assigned as the track number in the MP3 metadata during formatting.

It is highly recomended that AudioNFTs comprised of multiple audio files include a track number in their
filename, and metadata. 
TrackNumber Artist - Song Title.mp3
Ex: 1 DJCatskillNFT - Speedy-go-go.mp3
Ex: 2 Herr Doktor - Can You Kiss Me First.mp3