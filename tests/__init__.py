import vcr

tap_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/vcr_cassettes',
    record_mode='new_episodes',
    match_on=['uri', 'method'],
)
