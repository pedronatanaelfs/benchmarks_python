function eval_mpmop_value(value_id, t, xin_csv, xout_csv)
  x = dlmread(xin_csv);
  f = MPMOP_Value(value_id, x, t);
  dlmwrite(xout_csv, f, 'precision', 16);
end
