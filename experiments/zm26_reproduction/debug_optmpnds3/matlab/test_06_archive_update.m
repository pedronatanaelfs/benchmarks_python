function test_06_archive_update()
    P = setup_diag();
    G = ensure_global('MPDMP1', 20, 100000);
    seedX = diag_load_csv(fullfile(P.shared, 'archive_seed_X.csv'));
    insX = diag_load_csv(fullfile(P.shared, 'archive_insert_X.csv'));
    Archive = INDIVIDUAL(seedX);
    n_max = 8;
    sizes = zeros(size(insX,1)+1, 2);
    sizes(1,:) = [0, length(Archive)];
    for i = 1:size(insX,1)
        Archive = updateArchiveLocal(Archive, INDIVIDUAL(insX(i,:)), n_max);
        sizes(i+1,:) = [i, length(Archive)];
    end
    diag_write_csv(fullfile(P.out, 'test_06_archive_update.csv'), {'step','archive_size'}, sizes);
    diag_write_csv(fullfile(P.out, 'test_06_archive_final_X.csv'), {'x1','x2'}, Archive.decs);
    fprintf('matlab test_06 done final_n=%d\n', length(Archive));
end

function Archive = updateArchiveLocal(Archive, Population, N)
    for i = Population
        if length(Archive) < N
            Archive = [Archive, i];
        else
            decs = Archive.decs;
            dec = i.decs;
            dis = pdist2(decs, dec);
            [~, index] = min(dis);
            Archive(index) = i;
        end
    end
end
