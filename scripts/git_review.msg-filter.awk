#!/usr/bin/awk -f

BEGIN { have_attributions = 0 ; has_mine = 0; IGNORECASE = 1  }

{
    is_mine = 0
    if ($0 ~ /^[[:space:]]*(Signed-off|Reviewed)-by:/) {
        new_regex = "^[[:space:]]*(Signed-off|Reviewed)-by: " tag
        if ($0 ~ new_regex) {
            is_mine = 1
        }
        have_attributions = 1
    } else {
        if (have_attributions && !has_mine) {
            printf "Reviewed-by: %s\n", tag
            have_attributions = 0
            has_mine = 1
        }
    }
    if (is_mine && has_mine) {
        # do nothing
    } else {
	if (is_mine) {
	    has_mine = 1
        }
	print
    }
}

END {
    if (have_attributions && !has_mine) {
        printf "Reviewed-by: %s\n", tag
    }
}
