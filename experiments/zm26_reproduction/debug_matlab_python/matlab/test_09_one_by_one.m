function test_09_one_by_one()
%TEST_09_ONE_BY_ONE  OptMPNDS oneshot crowding vs OptMPNDS3 iterative entropy.
    P = setup_diag();
    F = diag_load_csv(fullfile(P.shared, 'lastfront_F.csv'));
    n = size(F, 1);
    KEEP = 5;
    front = ones(1, n);
    cd = CrowdingDistance(F, front);
    [~, order] = sort(cd, 'descend');
    keep = sort(order(1:KEEP));
    diag_write_csv(fullfile(P.out, 'test_09_optmpnds_oneshot.csv'), ...
        {'kept_1based','crowding'}, [keep(:), cd(keep)']);

    % OptMPNDS3-style: remove worst entropy one-by-one (does not call
    % OptMPNDS3/EnvironmentalSelection.m so the OptMPNDS path stays first).
    Last = 1:n;
    trace = [];
    it = 0;
    while numel(Last) > KEEP
        it = it + 1;
        ce = CrowdingEntropy(F(Last, :), ones(1, numel(Last)));
        [vmin, index] = min(ce);
        removed = Last(index);
        Last(index) = [];
        % remaining_after encoded as a decimal concat is awkward; write a sidecar
        trace = [trace; it, removed, vmin, numel(Last)]; %#ok<AGROW>
        fid = fopen(fullfile(P.out, sprintf('test_09_remaining_iter%d.csv', it)), 'w');
        fprintf(fid, 'remaining_1based\n');
        fprintf(fid, '%d\n', Last);
        fclose(fid);
    end
    diag_write_csv(fullfile(P.out, 'test_09_optmpnds3_iterative.csv'), ...
        {'iteration','candidate_removed_1based','entropy_of_removed','n_remaining'}, trace);
    fprintf('matlab test_09 done  iterative_steps=%d\n', size(trace,1));
end
