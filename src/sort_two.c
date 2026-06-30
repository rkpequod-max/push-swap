/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_two.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int             move_pivot(t_pile **p1, t_pile **p2, int ispa, t_pivot v)
{
        int     pivot;

        pivot = median_between(*p1, v.min, v.max);
        while (*p1 && are_left(*p1, pivot, ispa, v))
        {
                if (ispa)
                {
                        if (v.min <= (*p1)->x && (*p1)->x < pivot)
                                pab(p1, p2, "pb\n", v.op);
                        else
                                rab(p1, "ra\n", v.op);
                }
                else
                {
                        if ((*p1)->x >= pivot)
                                pab(p1, p2, "pa\n", v.op);
                        else
                                rab(p1, "rb\n", v.op);
                }
        }
        return (pivot);
}

void    quick_return(t_pile **p, t_pivot v)
{
        while (last_between(*p, v.min, v.max))
                rrab(p, "rra\n", v.op);
}

void    pass_limits(t_pile **pa, t_pile **pb, int i, int op)
{
        int             minpos;
        int             maxpos;
        t_pile  *p;

        p = *pa;
        while (p)
        {
                if (p->x == pile_max(*pa))
                        maxpos = i;
                if (p->x == pile_min(*pa))
                        minpos = i;
                i++;
                p = p->next;
        }
        i = pile_len(*pa);
        maxpos = (ft_abs(maxpos - i) < maxpos) ? -ft_abs(maxpos - i) : maxpos;
        minpos = (ft_abs(minpos - i) < minpos) ? -ft_abs(minpos - i) : minpos;
        minpos = (ft_abs(minpos) > ft_abs(maxpos)) ? maxpos : minpos;
        while (minpos != 0)
        {
                (minpos < 0) ? rrab(pa, "rra\n", op) : rab(pa, "ra\n", op);
                minpos += (minpos < 0) ? 1 : -1;
        }
        pab(pa, pb, "pb\n", op);
        (pile_len(*pa) == 4) ? pass_limits(pa, pb, 0, op) : 0;
}

void    insert_pile(t_pile **pa, t_pile **pb, int op)
{
        pab(pb, pa, "pa\n", op);
        if (ordered(*pa, 1) && (*pb))
                insert_pile(pa, pb, op);
        else
        {
                if (!ordered(*pa, 1))
                        rab(pa, "ra\n", op);
                if (*pb)
                        insert_pile(pa, pb, op);
        }
}

void    mini_solve(t_pile **pa, t_pile **pb, int op)
{
        int p1;
        int p2;

        if (pile_len(*pa) <= 3)
        {
                p1 = (*pa)->x;
                p2 = (*pa)->next->x;
                if (p1 > p2 || (p1 == pile_min(*pa) && p2 == pile_max(*pa)))
                {
                        if (p1 == pile_max(*pa) && p2 == pile_min(*pa))
                                rab(pa, "ra\n", op);
                        else
                                sab(pa, "sa\n", op);
                }
                else
                        rrab(pa, "rra\n", op);
                if (!ordered(*pa, 1))
                        mini_solve(pa, pb, op);
                return ;
        }
        pass_limits(pa, pb, 0, op);
        mini_solve(pa, pb, op);
        insert_pile(pa, pb, op);
}

/* ═══ Cost-based insertion sort — optimal for large stacks ═══ */

/* Find position in circular sorted A where val should be inserted */
/* A is sorted but may be rotated — min_val is somewhere in the middle */
static int  find_insert_pos(t_pile *pa, int val)
{
        int max_val;
        int min_pos;
        int len;
        int i;
        int arr[10000];
        t_pile *tmp;

        if (!pa)
                return (0);
        tmp = pa;
        len = 0;
        while (tmp && len < 10000)
        {
                arr[len] = tmp->x;
                len++;
                tmp = tmp->next;
        }
        max_val = arr[0];
        min_pos = 0;
        i = 0;
        while (i < len)
        {
                if (arr[i] < arr[min_pos])
                        min_pos = i;
                if (arr[i] > max_val)
                        max_val = arr[i];
                i++;
        }
        if (val < arr[min_pos] || val > max_val)
                return (min_pos);
        /* Walk sorted order starting from min_pos */
        i = 0;
        while (i < len)
        {
                int idx = (min_pos + i) % len;
                if (arr[idx] > val)
                        return (idx);
                i++;
        }
        return (min_pos);
}

/* Sort exactly 3 elements in A (minimal ops) */
static void sort_three(t_pile **pa, int op)
{
        int a = (*pa)->x;
        int b = (*pa)->next->x;
        int c = (*pa)->next->next->x;

        if (a > b && b < c && a < c)
                sab(pa, "sa\n", op);
        else if (a > b && b > c)
        {
                sab(pa, "sa\n", op);
                rrab(pa, "rra\n", op);
        }
        else if (a > b && b < c && a > c)
                rab(pa, "ra\n", op);
        else if (a < b && b > c && a < c)
        {
                sab(pa, "sa\n", op);
                rab(pa, "ra\n", op);
        }
        else if (a < b && b > c && a > c)
                rrab(pa, "rra\n", op);
}

/* Cost-based sort: push to B, then insert back optimally */
void    cost_sort(t_pile **pa, t_pile **pb, int op)
{
        int len_a, len_b;
        int i, best_i;
        int target, best_cost, cost;
        int ra, rra, rb, rrb;
        int min_val;
        t_pile *tmp;

        /* Push all but 3 to B */
        while (pile_len(*pa) > 3)
                pab(pa, pb, "pb\n", op);
        /* Sort 3 remaining */
        sort_three(pa, op);
        min_val = pile_min(*pa);

        /* Insert each element from B back to A with minimal cost */
        while (*pb)
        {
                len_a = pile_len(*pa);
                len_b = pile_len(*pb);
                best_cost = 999999;
                best_i = 0;

                tmp = *pb;
                i = 0;
                while (i < len_b)
                {
                        target = find_insert_pos(*pa, tmp->x);
                        ra = target;
                        rra = len_a - target;
                        rb = i;
                        rrb = len_b - i;

                        /* 4 strategies: rr, rrr, ra+rrb, rra+rb */
                        {
                                int c_rr = ((ra > rb) ? ra : rb) + 1;
                                int c_rrr = ((rra > rrb) ? rra : rrb) + 1;
                                int c_mix1 = ra + rrb + 1;
                                int c_mix2 = rra + rb + 1;
                                cost = c_rr;
                                if (c_rrr < cost) cost = c_rrr;
                                if (c_mix1 < cost) cost = c_mix1;
                                if (c_mix2 < cost) cost = c_mix2;
                        }

                        if (cost < best_cost)
                        {
                                best_cost = cost;
                                best_i = i;
                        }
                        tmp = tmp->next;
                        i++;
                }

                /* Recalculate for best element */
                tmp = *pb;
                i = 0;
                while (i < best_i) { tmp = tmp->next; i++; }
                target = find_insert_pos(*pa, tmp->x);
                ra = target; rra = len_a - target;
                rb = best_i; rrb = len_b - best_i;

                {
                        int c_rr = ((ra > rb) ? ra : rb) + 1;
                        int c_rrr = ((rra > rrb) ? rra : rrb) + 1;
                        int c_mix1 = ra + rrb + 1;
                        int c_mix2 = rra + rb + 1;

                        /* Execute cheapest strategy */
                        if (c_rr <= c_rrr && c_rr <= c_mix1 && c_rr <= c_mix2)
                        {
                                /* Use rr for common rotations, then individual */
                                while (ra > 0 && rb > 0)
                                {
                                        ft_putstr("rr\n");
                                        rab(pa, "", op);
                                        rab(pb, "", op);
                                        ra--; rb--;
                                }
                                while (ra > 0) { rab(pa, "ra\n", op); ra--; }
                                while (rb > 0) { rab(pb, "rb\n", op); rb--; }
                        }
                        else if (c_rrr <= c_mix1 && c_rrr <= c_mix2)
                        {
                                while (rra > 0 && rrb > 0)
                                {
                                        ft_putstr("rrr\n");
                                        rrab(pa, "", op);
                                        rrab(pb, "", op);
                                        rra--; rrb--;
                                }
                                while (rra > 0) { rrab(pa, "rra\n", op); rra--; }
                                while (rrb > 0) { rrab(pb, "rrb\n", op); rrb--; }
                        }
                        else if (c_mix1 <= c_mix2)
                        {
                                while (ra > 0) { rab(pa, "ra\n", op); ra--; }
                                while (rrb > 0) { rrab(pb, "rrb\n", op); rrb--; }
                        }
                        else
                        {
                                while (rra > 0) { rrab(pa, "rra\n", op); rra--; }
                                while (rb > 0) { rab(pb, "rb\n", op); rb--; }
                        }
                }
                pab(pb, pa, "pa\n", op);
                /* Update min_val if we just inserted a new minimum */
                if ((*pa)->x < min_val)
                        min_val = (*pa)->x;
        }

        /* Final: rotate A to put min at top (shortest direction) */
        {
                int pos = 0;
                int len = pile_len(*pa);
                tmp = *pa;
                while (tmp && tmp->x != min_val) { pos++; tmp = tmp->next; }
                if (pos <= len / 2)
                        while ((*pa)->x != min_val) rab(pa, "ra\n", op);
                else
                        while ((*pa)->x != min_val) rrab(pa, "rra\n", op);
        }
}
