def incremental_search_method(f, xl, increment, tol, max_iter):
    steps = []
    
    curr_x = round(float(xl), 6)
    curr_inc = round(float(increment), 6)
    tol = round(float(tol), 6)
    
    pass_num = 1
    
    # Outer loop: Keep creating new tables until the increment is smaller than the tolerance
    while curr_inc >= tol and pass_num <= max_iter:
        step_num = 1
        x_val = curr_x
        
        # Inner loop: Step forward until we find a sign change
        while True:
            fx_val = round(float(f(x_val)), 6)
            next_x = round(x_val + curr_inc, 6)
            next_fx = round(float(f(next_x)), 6)
            
            # Record the current step
            steps.append({
                "Table Pass": f"Iteration {pass_num}",
                "Iter No.": step_num,
                "x": f"{x_val:.6f}",
                "f(X)": f"{fx_val:.6f}"
            })
            
            # Check for a sign change
            if fx_val * next_fx <= 0:
                # Record the final bound where the sign change occurred (to complete the bracket)
                steps.append({
                    "Table Pass": f"Iteration {pass_num}",
                    "Iter No.": step_num + 1,
                    "x": f"{next_x:.6f}",
                    "f(X)": f"{next_fx:.6f}"
                })
                
                # Zoom in for the next table pass
                curr_x = x_val                       # Step back to the lower bound
                curr_inc = round(curr_inc / 10.0, 6) # Shrink the increment by dividing by 10
                break                                # Break the inner loop to start the next table
                
            # Move forward if no sign change
            x_val = next_x
            step_num += 1
            
            # Failsafe: Prevent infinite loops if there is no root
            if step_num > 1000:
                return steps, "Error: No sign change found within limits."
                
        pass_num += 1
        
    # Calculate the final approximate root (midpoint of the very last, tiniest bracket)
    final_root = round((x_val + next_x) / 2.0, 6)
    
    return steps, f"Approx Root: {final_root:.6f}"