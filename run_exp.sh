set -x
arr=$(ls ./"$@")
for job in $arr; do
  python3 ./make_input.py "$@"/$job
done


for task in $arr; do
  job=${task%%.txt}
  job=${job##dag/}
  ((time timeout 1800 glpsol --cpxlp --first "solver_inputs/"$job"_default_input.lp" -o "solver_outputs/"$job"_default_output.txt" > "outputs/"$job"output_default.txt") 2>"times/"$job"_default_time" 1>/dev/null) &
  ((time timeout 1800 glpsol --cpxlp --first "solver_inputs/"$job"_reverse_tiers_input.lp" -o "solver_outputs/"$job"_reverse_tiers_output.txt" > "outputs/"$job"reverse_tiers_output.txt") 2>"times/"$job"_reverse_tiers_time" 1>/dev/null) &
  ((time timeout 1800 glpsol --cpxlp --first "solver_inputs/"$job"_tiers_input.lp" -o "solver_outputs/"$job"_tiers_output.txt" > "outputs/"$job"output_tiers.txt") 2>"times/"$job"_tiers_time" 1>/dev/null) &
  ((time timeout 1800 glpsol --cpxlp --first "solver_inputs/"$job"_up_right_input.lp" -o "solver_outputs/"$job"_up_right_output.txt" > "outputs/"$job"output_up_right.txt") 2>"times/"$job"_up_right_time" 1>/dev/null)  &
  ((time timeout 1800 glpsol --cpxlp --first "solver_inputs/"$job"_down_left_input.lp" -o "solver_outputs/"$job"_down_left_output.txt" > "outputs/"$job"output_down_left.txt") 2>"times/"$job"_down_left_time" 1>/dev/null);
done
