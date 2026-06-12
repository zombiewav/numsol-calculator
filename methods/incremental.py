def incremental_search_method(f, xl, increment, tol, max_iter):
    steps = []
    
    curr_x = round(float(xl), 6)
    curr_inc = round(float(increment), 6)
    tol = round(float(tol), 6)
    
    cluster_num = 1
    
    # Outer loop: Keep creating new clusters until the tolerance condition is satisfied
    while cluster_num <= max_iter:
        step_num = 1
        x_val = curr_x
        
        # Inner loop: Step forward until we find a sign change
        while True:
            fx_val = round(float(f(x_val)), 6)
            next_x = round(x_val + curr_inc, 6)
            next_fx = round(float(f(next_x)), 6)
            
            # Record the current step
            steps.append({
                "Table Pass": f"Cluster {cluster_num}",
                "Iter No.": step_num,
                "x": f"{x_val:.6f}",
                "f(X)": f"{fx_val:.6f}"
            })
            
            # Check for a sign change
            if fx_val * next_fx <= 0:
                # Record the final bound where the sign change occurred (to complete the bracket)
                steps.append({
                    "Table Pass": f"Cluster {cluster_num}",
                    "Iter No.": step_num + 1,
                    "x": f"{next_x:.6f}",
                    "f(X)": f"{next_fx:.6f}"
                })
                
                # Check the tolerance condition: use the endpoint with smaller absolute value
                if abs(fx_val) < abs(next_fx):
                    tolerance_check = abs(fx_val)
                else:
                    tolerance_check = abs(next_fx)
                
                if tolerance_check < tol:
                    # Tolerance satisfied: stop and compute the final root
                    final_root = round((x_val + next_x) / 2.0, 6)
                    return steps, f"Approx Root: {final_root:.6f}"
                
                # Tolerance not satisfied: Create a new cluster
                # Use the sign change interval as the new search interval
                curr_x = x_val                       # Step back to the lower bound
                curr_inc = round(curr_inc / 10.0, 6) # Reduce the increment by a factor of 10
                cluster_num += 1
                break                                # Break the inner loop to start the next cluster
                
            # Move forward if no sign change
            x_val = next_x
            step_num += 1
            
            # Failsafe: Prevent infinite loops if there is no root
            if step_num > 1000:
                return steps, "Error: No sign change found within limits."
                
    return steps, "Error: Max iterations reached without satisfying tolerance."