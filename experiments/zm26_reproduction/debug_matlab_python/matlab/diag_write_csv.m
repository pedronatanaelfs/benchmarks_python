function diag_write_csv(path, header, data)
%DIAG_WRITE_CSV  Write a CSV with a header row. Inf/NaN are explicit.
    fid = fopen(path, 'w');
    if fid < 0
        error('Cannot write %s', path);
    end
    cleanup = onCleanup(@() fclose(fid));
    if iscell(header)
        fprintf(fid, '%s\n', strjoin(header, ','));
    else
        fprintf(fid, '%s\n', header);
    end
    if isempty(data)
        return;
    end
    [n, m] = size(data);
    for i = 1:n
        for j = 1:m
            if j > 1
                fprintf(fid, ',');
            end
            v = data(i, j);
            if isinf(v)
                if v > 0
                    fprintf(fid, 'Inf');
                else
                    fprintf(fid, '-Inf');
                end
            elseif isnan(v)
                fprintf(fid, 'NaN');
            else
                fprintf(fid, '%.16g', v);
            end
        end
        fprintf(fid, '\n');
    end
end
