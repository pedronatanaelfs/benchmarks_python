function dump_nsidedpoly(out_csv)
  cases = {
    'MPDMP3_tri', nsidedpoly_vertices(3, [50,40], 'Radius', 20);
    'MPDMP5_p1', nsidedpoly_vertices(3, [39,40], 'Radius', 40);
    'MPDMP5_p2', nsidedpoly_vertices(3, [60,20], 'Radius', 40);
    'MPDMP6_p1', nsidedpoly_vertices(4, [38,50], 'SideLength', 24);
    'MPDMP6_p2', nsidedpoly_vertices(4, [60,50], 'SideLength', 20);
    'MPDMP7_p1', nsidedpoly_vertices(4, [30,50], 'SideLength', 40);
    'MPDMP7_p2', nsidedpoly_vertices(4, [60,40], 'SideLength', 40);
    'MPDMP8_p1', nsidedpoly_vertices(5, [40,50], 'Radius', 20);
    'MPDMP8_p2', nsidedpoly_vertices(5, [60,45], 'Radius', 20);
    'MPDMP10_sq', nsidedpoly_vertices(4, [50,50], 'SideLength', 30);
    'MPDMP11_p1', nsidedpoly_vertices(3, [30,40], 'Radius', 20);
    'MPDMP11_p2', nsidedpoly_vertices(3, [50,40], 'Radius', 20);
    'MPDMP11_p3', nsidedpoly_vertices(3, [40,45], 'Radius', 20);
    'MPDMP12_p1', nsidedpoly_vertices(4, [30,40], 'Radius', 20);
    'MPDMP12_p2', nsidedpoly_vertices(4, [50,40], 'Radius', 20);
    'MPDMP12_p3', nsidedpoly_vertices(4, [40,50], 'Radius', 20);
  };
  fid = fopen(out_csv, 'w');
  fprintf(fid, 'name,i,x,y\n');
  for c = 1:size(cases,1)
    name = cases{c,1};
    V = cases{c,2};
    for i = 1:size(V,1)
      fprintf(fid, '%s,%d,%.16g,%.16g\n', name, i, V(i,1), V(i,2));
    end
  end
  fclose(fid);
end
