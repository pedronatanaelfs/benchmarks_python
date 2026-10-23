function test_03_crowding()
%TEST_03_CROWDING  Original CrowdingDistance.m and CrowdingEntropy.m.
    P = setup_diag();
    F = diag_load_csv(fullfile(P.shared, 'crowding_F.csv'));
    front = diag_load_csv(fullfile(P.shared, 'crowding_front.csv'));
    front = front(:)';
    cd = CrowdingDistance(F, front);
    ce = CrowdingEntropy(F, front);
    n = size(F, 1);
    data = [(1:n)', front(:), cd(:), ce(:)];
    diag_write_csv(fullfile(P.out, 'test_03_crowding.csv'), ...
        {'point_id','front','crowding_value','entropy_value'}, data);
    fprintf('matlab test_03 done\n');
end
