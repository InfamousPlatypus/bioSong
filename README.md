# bioSong
A tool for getting xeno-canto bird calls and transforming them for use in TensorFlow


bioSong is a work in progress. There is currently no error checking. Use at your own risk

bioSong connects to the Xeno-Canto API allowing batch downloading of bird calls from a specific species or cournty. Sub-species is currently not allowed.
    .mp3 files are downloaded for user specified search criteria

    .mp3 files are converted to .wav

    48k wave files are downsampled to 44.1k
    only 44.1k files are processed all others are currently ignored
    wav files are segmented into 500ms samples with a 150ms offset
    these 500ms samples are processed with a scipy STFT using a Hann window with a
        window size of 512 and a step size of 256 for 50% overlap
    .png files are outputted for each window to be used in TensorFlow for image recognition
