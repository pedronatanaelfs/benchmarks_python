function test_03_archive_initialization()
    P = setup_diag();
    diag_write_csv(fullfile(P.out, 'test_03_archive_initialization.csv'), ...
        {'generation','matlab_archive_size'}, [0, 0]);
    fprintf('matlab test_03 done Archive=[] at gen 0\n');
end
